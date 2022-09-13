import flask
import json
import enum
from application import app, db, bcrypt
from flask import jsonify, request, session, make_response
from application.models import SocialUser, Auth, Post , likes , dislikes, Comment
from application.auth import encode_func, decode_func
from functools import wraps
from flask_cors import cross_origin


class StatusCode(enum.Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500
    UNAUTHORIZED = 401


def authorized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("calling decorator")
        decode_data, token = decode_func()
        if 'Error' in decode_data:
            return jsonify({"Error ": "The token has expired Login again"}), StatusCode.BAD_REQUEST.value
        if not decode_data:
            return jsonify({"failure": "Invalid token "}), StatusCode.BAD_REQUEST.value
        headers = flask.request.headers
        bearer = headers.get('Authorization')
        token = bearer.split()[1]
        social_user = SocialUser.query.filter_by(username=decode_data.get('username')).first()
        author = Auth.query.filter_by(user_id=social_user.id).first()
        if token != author.auth_token:
            return jsonify({"Failure": "Invalid Token"}), StatusCode.BAD_REQUEST.value
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
@app.route('/home')
def home_page():
    return jsonify({"hello":"this is home page"})


@app.route('/register', methods =['POST'])
@cross_origin()
def register_user():
    try:
        username = request.json.get('username')
        social_user_obj = SocialUser.query.filter_by(username=username).first()
        print(social_user_obj)
        if social_user_obj != None:
            return jsonify({"Error": "This username already exists "}), StatusCode.BAD_REQUEST.value
        email = request.json.get('email')
        social_user_obj = SocialUser.query.filter_by(email=email).first()
        print(social_user_obj)
        if social_user_obj != None:
            return jsonify({"Error" : "This email already exists "}), StatusCode.BAD_REQUEST.value
        password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8')
        user1 = SocialUser(username=username, email=email, password=password)
        db.session.add(user1)
        db.session.commit()
        return jsonify({"response": "The user created successfully",
                        "status": "Written into databases"}), StatusCode.OK.value
    except Exception as e:
        return jsonify({"Error": "Error occurred in register user"}), StatusCode.BAD_REQUEST.value


@app.route('/getuser', methods=['GET'])
@cross_origin()
@authorized
def get_user():
    try:
        decode_data, token = decode_func()
        social_user = SocialUser.query.filter_by(username=decode_data.get('username')).first()
        user_dic = {"Id": social_user.id, "Username": social_user.username, "Email": social_user.email, "Age": social_user.age, "gender": social_user.gender, "Posts": len(social_user.posts)}
        return jsonify(user_dic), StatusCode.OK.value
    except Exception as e:
        return jsonify({"Error": "Error occurred in getting posts"}), StatusCode.BAD_REQUEST.value


@app.route('/login', methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    try:
        print("calling")
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        print(username, password)
        social_user_object = SocialUser.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(social_user_object.password, password) and social_user_object.username == username:
            access_token = encode_func()
            author = Auth.query.filter_by(user_id=social_user_object.id).first()
            if author is None:
                author1 = Auth(user_id=social_user_object.id, auth_token=access_token)
                db.session.add(author1)
            else:
                author1 = Auth.query.filter_by(user_id=social_user_object.id).first()
                author1.auth_token=access_token
            db.session.commit()
            return jsonify(access_token=access_token)
        else:
            return jsonify({"failure": "Wrong id or password "}), StatusCode.UNAUTHORIZED.value
    except Exception as e:
        return jsonify({"Error": "Error in login"}), StatusCode.BAD_REQUEST.value


@app.route('/createpost', methods=['POST'])
@cross_origin()
@authorized
def create_post():
    try:
        print("calling createpost")
        post_title = request.json.get("title",None)
        post_content = request.json.get("content",None)
        decode_data, token = decode_func()
        social_user = SocialUser.query.filter_by(username=decode_data.get('username')).first()
        post = Post(title=post_title, content=post_content, social_user_id=social_user.id)
        db.session.add(post)
        db.session.commit()
        return jsonify({"Success": "Post Created Successfully"}), StatusCode.OK.value
    except Exception as e:
        return jsonify({"Error ": "Error in creating post"}), StatusCode.BAD_REQUEST.value


@app.route('/getmypost', methods=['GET'])
@cross_origin()
@authorized
def get_my_post():
    try:
        decode_data , token = decode_func()
        social_user = SocialUser.query.filter_by(username=decode_data.get('username')).first()
        user_posts = Post.query.filter_by(social_user_id = social_user.id).all()
        if user_posts is None:
            return jsonify({"Message": "You have not posted any content"}), StatusCode.OK.value
        lst_posts = []
        for post in user_posts:
            lst_comments = []
            lst_users_liked = []
            lst_users_disliked = []
            for user in post.liked_by:
                like_user_dic = {"id": user.id, "name": user.username }
                lst_users_liked.append(like_user_dic)
            for user in post.disliked_by:
                dislike_user_dic = {"id ": user.id, "name": user.username}
                lst_users_disliked.append(dislike_user_dic)
            for comment in post.comments:
                dic_comment = {"cid":comment.id , "content":comment.content, "User_id":comment.user_id , "date":comment.date_posted}
                lst_comments.append(dic_comment)
            # for comment in post.comments:
            #     lst_comment.append(comment.content)
            post_dic = {"id": post.post_id, "title": post.title, "content": post.content, "likes_count": len(post.liked_by) , "dislikes_count":len(post.disliked_by) ,"comments_by":lst_comments,"liked_by":lst_users_liked,"disliked_by":lst_users_disliked}
            lst_posts.append(post_dic)
        return jsonify({"posts": lst_posts}), StatusCode.OK.value
    except Exception as e:
        print(e)
        return jsonify({"Error ": "Error in getting posts"}), StatusCode.BAD_REQUEST.value


@app.route('/editprofile', methods=['POST'])
@cross_origin()
@authorized
def edit_profile():
    try:
        age = request.json.get("age")
        gender = request.json.get("gender")
        decode_data, token = decode_func()
        social_user = SocialUser.query.filter_by(username=decode_data.get('username')).first()
        social_user.age = age
        social_user.gender = gender
        db.session.commit()
        return jsonify({"Success": "Profile updated successfully"}), StatusCode.OK.value
    except Exception as e:
        return jsonify({"Error": "Error in updating profile"}), StatusCode.BAD_REQUEST.value


@app.route('/getposts', methods=['GET'])
@cross_origin()
@authorized
def getPosts():
    try:
        print("calling")
        social_posts_obj = Post.query.all()
        posts_list =[]
        dic = {}
        for post in social_posts_obj:
            lst_users_liked = []
            lst_users_disliked = []
            lst_comments = []
            temp = post.__dict__
            temp['likes_count'] = len(post.liked_by)
            temp['dislike_count']= len(post.disliked_by)
            for user in post.liked_by:
                like_user_dic = {"id ": user.id, "name ": user.username }
                lst_users_liked.append(like_user_dic)
            for user in post.disliked_by:
                dislike_user_dic = {"id ": user.id, "name": user.username}
                lst_users_disliked.append(dislike_user_dic)
            for comment in post.comments:
                dic_comment = {"cid":comment.id , "content":comment.content, "User_id":comment.user_id , "date":comment.date_posted}
                lst_comments.append(dic_comment)
            del temp['__ts_vector__']
            del temp['liked_by']
            del temp['disliked_by']
            del temp['_sa_instance_state']
            del temp['comments']
            temp['liked_by'] = lst_users_liked
            temp['disliked_by'] = lst_users_disliked
            temp['comments_by'] = lst_comments
            posts_list.append(temp)
            print(temp)
        return jsonify({"posts" : posts_list}), StatusCode.OK.value
    except Exception as e:
        print(e)
        return jsonify({"Error ": "Error Occurred in getting posts"}), StatusCode.BAD_REQUEST.value


@app.route('/likeposts', methods=['POST'])
@cross_origin()
@authorized
def like_post():
    try:
        print("calling like function ")
        post_id = request.json.get("postid")
        decode_data, token = decode_func()
        recent_post = Post.query.filter_by(post_id=post_id).first()
        if recent_post == None:
            return jsonify({"Error": "The post id you entered is incorrect "}), 400
        social_user = SocialUser.query.filter_by(username=decode_data.get('username')).first()
        if social_user in recent_post.disliked_by:
            db.session.query(dislikes).filter_by(post_id=post_id, user_id=social_user.id).delete()
            db.session.commit()
        social_user.liked.append(recent_post)
        db.session.commit()
        return jsonify({"Success": "Post Liked"}), StatusCode.OK.value
    except Exception as e:
        return jsonify({"Error ": "error in liking post"}), StatusCode.BAD_REQUEST


@app.route('/dislikeposts', methods=['POST'])
@cross_origin()
@authorized
def dislike_post():
    try:
        post_id = request.json.get("postid")
        decode_data , token = decode_func()
        recent_post = Post.query.filter_by(post_id=post_id).first()
        if recent_post == None:
            return jsonify({"Error": "The post id you entered is incorrect"}) , StatusCode.BAD_REQUEST
        social_user = SocialUser.query.filter_by(username = decode_data.get('username')).first()
        if social_user in recent_post.liked_by:
            db.session.query(likes).filter_by(post_id=post_id, user_id=social_user.id).delete()
            db.session.commit()
        social_user.disliked.append(recent_post)
        db.session.commit()
        return jsonify({"Success": "Post Disliked successfully"}), StatusCode.OK.value
    except Exception as e:
        return jsonify({"Error": "Error in disliking post"}), StatusCode.BAD_REQUEST.value


@app.route('/search_post', methods=['POST'])
@cross_origin()
@authorized
def search_post():
    try:
        print("calling search post")
        post_keyword = request.json.get('search_keyword', None)
        keyword_list = list(post_keyword.split())
        posts_obj = Post.query.filter(Post.__ts_vector__.match(post_keyword)).all()
        post_list = []
        for post in posts_obj:
            post_dic = {"id":post.post_id, "title":post.title, "content":post.content, "userId":post.social_user_id}
            post_list.append(post_dic)
        if len(post_list) == 0:
            return jsonify({"Message": "There is no post related to this keyword"})
        return jsonify({"posts": post_list}), StatusCode.OK.value
    except Exception as e:
        print(e)
        return jsonify({"Error": "Error in searching posts"}), StatusCode.BAD_REQUEST.value


@app.route('/get_by_index', methods=['GET'])
@cross_origin()
@authorized
def get_by_index():
    try:
        start = int(request.args.get('start'))
        limit = int(request.args.get('limit'))
        if start > limit:
            return jsonify({"Message":"Enter valid indexes"}), StatusCode.BAD_REQUEST.value
        posts = Post.query.all()
        posts = posts[start:limit+1]
        post_list = []
        for post in posts:
            post_dic = {'id':post.post_id, 'title':post.title, 'content':post.content}
            post_list.append(post_dic)
        if len(post_list) == 0:
            return jsonify({"Message": "No posts to display"})
        return jsonify({"posts": post_list}), StatusCode.OK.value
    except Exception as e:
        return jsonify({"Error":"Error in getting posts"}), StatusCode.BAD_REQUEST.value


@app.route('/comment', methods=["POST"])
@cross_origin()
@authorized
def comment():
    try:
        print("calling comment function")
        post_id = request.json.get('postid', None)
        comment = request.json.get('comment', None)
        decode_data , token = decode_func()
        social_user_obj = SocialUser.query.filter_by(username=decode_data.get('username')).first()
        comment = Comment(content=comment, post_id=post_id, user_id=social_user_obj.id)
        db.session.add(comment)
        db.session.commit()
        return jsonify({"Success": "Comment added successfully"})
    except Exception as e:
        return jsonify({"Error":"Error in adding comment to post"})
