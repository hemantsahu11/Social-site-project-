console.log("this is login js ");

// login function
function login_function(){
    console.log("inside login function")
    url= "http://localhost:8000/login";

    const data = new FormData();
    data["username"]= document.getElementById("username").value;
    data["password"] = document.getElementById("password").value;
    params = {
        method:"POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type' :'application/json'
        },
        body: JSON.stringify(data)
    }
    fetch(url,params)
    .then( (response) => {
    if (response.status === 200) {
        window.location.href = "../templates/user.html"
        return response.json()
    }
    else if(response.status === 401){
        console.log("Incorrect Password")
        var mainContainer = document.getElementById("IncorrectPassword");
            var div = document.createElement("div")
            div.innerHTML = "Incorrect username or password";
            mainContainer.appendChild(div);
    }
    else {
        throw Error('Something went wrong ;')
    }
})
.then( (data) => {
    sessionStorage.setItem("token","token "+data['access_token'])
    console.log(data)
    return data
})
.catch( (error) => {
    console.log(`Catch: ${error}`)
})
}


// register function
function register_function(){
    console.log("inside register function")
    url= "http://localhost:8000/register";
    const data = new FormData();
    data["username"]= document.getElementById("username").value;
    data["email"] = document.getElementById("mail").value;
    data["password"] = document.getElementById("password").value;

    params = {
        method:"POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type' :'application/json'
        },
        body: JSON.stringify(data)
    }
    fetch(url,params)
    .then( (response) => {
    if (response.status === 200) {
        window.location.href="../templates/login.html";
        return response.json()
    } else {
        throw Error('Something went wrong ;')
    }
})
.then( (data) => {
    console.log(data)
    return data
})
.catch( (error) => {
    console.log(`Catch: ${error}`)
})

}


// function for gettting posts
async function getPosts() {
//    var comment;
    console.log("calling get posts function");
    let url = 'http://localhost:8000/getposts';
    params = {
    method : 'GET',
    headers: {
      'Content-Type' : 'application/json',
      "Authorization": sessionStorage.getItem("token")
    }
    }
    try {
        let res = await fetch(url, params);
        posts = JSON.stringify(await res.json())
        console.log("print",posts)
        json = JSON.parse(posts);
        console.log(json)
        data = json["posts"];
        console.log("data",data)
        var mainContainer = document.getElementById("myText");
        for (var i =0;i<data.length;i++){
            var div = document.createElement("div")
              div.innerHTML =  `<div class="card w-70">
                          <div class="card-header w-70">
                            Post ${i+1}
                          </div>
                          <div class="card-body">
                            <div class="card-text">
                                 <p> Post Id : ${data[i].post_id} </p>
                               <p> Post title : ${data[i].title} </p>
                                 <p> Content : ${data[i].content}</p>
                                <p> Likes : ${data[i].likes_count} likes </p>
                                <p> Dislikes : ${data[i].dislike_count} </p>
                                <p> User's Id : ${data[i].social_user_id} </p>
                                <p> Comments : ${data[i].comments_by.map( c => c.content )} </p>
                            </div>
                            <button onclick="like_post(${data[i].post_id})" class="btn btn-primary" id=${'like' + i} style="margin-right: 20px; margin-bottom: 10px;">Like </button>
                            <button onclick="dislike_post(${data[i].post_id})" id=${'dislike'+ i} class="btn btn-danger" style="margin-bottom: 10px;">Dislike </button>
                            <br>
                            <input type="text" placeholder="Comment..." id=${'comment'+i} >
                            <button onclick="do_comment(${data[i].post_id},${i})" id=${'commentBtn'+ i} class="btn btn-info" style="margin-left: 15px;">Comment</button>
                          </div>
                        </div>`
            mainContainer.appendChild(div);
        }
        return posts;
    } catch (error) {
        console.log(error);
    }
}

// function for getting users post only
async function get_users_post(){
    console.log("calling get posts function");
    let url = 'http://localhost:8000/getmypost';
    params = {
    method : 'GET',
    headers: {
      'Content-Type' : 'application/json',
      "Authorization": sessionStorage.getItem("token")
    }
    }
    try {
        let res = await fetch(url, params);
        posts = JSON.stringify(await res.json())
        console.log("print",posts)
        json = JSON.parse(posts);
        console.log(json)
        data = json["posts"];
        console.log("data",data)
        var mainContainer = document.getElementById("ShowMyPost");
        for (var i =0;i<data.length;i++){
            var div = document.createElement("div")
              div.innerHTML = `<div class="card w-70">
              <div class="card-header w-70">Post ${i+1}</div>
              <div class="card-body">
                <p class="card-text"> Title : ${data[i].title} </p>
                <p class="card-text"> content : ${data[i].content} </p>
                <p class="card-text"> Comments : ${data[i].comments_by.map(c => "user-"+ c.User_id +": "+c.content)} </p>
                <p class="card-text"> Liked By : ${data[i].liked_by.map(c => c.name)} </p>
                <p class="card-text"> Disliked By : ${data[i].disliked_by.map(c => c.name)} </p>
              </div>
              <div class="card-footer text-muted">Likes: ${data[i].likes_count}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Dislikes: ${data[i].dislikes_count}</div>
              <br>
            </div>`
            mainContainer.appendChild(div);
        }
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}
// function for like posts
function like_post(postid)
{
    console.log("inside like function")
    url= "http://localhost:8000/likeposts";

    const data = new FormData();
    data["postid"] = postid
    params = {
        method:"POST",
        headers: {
            'Content-Type' :'application/json',
            "Authorization": sessionStorage.getItem("token")
        },
        body: JSON.stringify(data)
    }
    fetch(url,params)
    .then( (response) => {
    if (response.status === 200) {
        console.log("post liked successfully")
        return response.json()
    } else {
        throw Error('Something went wrong ;(')
    }
})
}

// function for dislike post
function dislike_post(postid)
{
    console.log("inside dislike function")
    url= "http://localhost:8000/dislikeposts";

    const data = new FormData();
    data["postid"] = postid
    params = {
        method:"POST",
        headers: {
            'Content-Type' :'application/json',
            "Authorization": sessionStorage.getItem("token")
        },
        body: JSON.stringify(data)
    }
    fetch(url,params)
    .then( (response) => {
    if (response.status === 200) {
        console.log("post disliked successfully")
        return response.json()
    } else {
        throw Error('Something went wrong ;')
    }
})
}

// function for logout
function logout(){
    console.log("calling logout function")
    sessionStorage.clear();
    window.location.href = "../templates/home.html"

}

// function createpost
function createPost(){
      console.log("inside createpost function")
    url= "http://localhost:8000/createpost";

    const data = new FormData();
    data["title"]= document.getElementById("TitleInput").value;
    data["content"] = document.getElementById("Textarea").value;
    params = {
        method:"POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type' :'application/json',
            "Authorization": sessionStorage.getItem("token")
        },
        body: JSON.stringify(data)
    }
    fetch(url,params)
    .then( (response) => {
    if (response.status === 200) {
        var mainContainer = document.getElementById("PrintSuccess");
            var div = document.createElement("div")
            div.innerHTML = "Post Created Successfully";
            mainContainer.appendChild(div);
        return response.json()
    } else {
        throw Error('Something went wrong ;')
    }
})
.then( (data) => {
    console.log(data)
    return data
})
.catch( (error) => {
    console.log(`Catch: ${error}`)
})
}

// function for edit profile
function edit_profile(){
    console.log("inside edit profile function")
    url= "http://localhost:8000/editprofile";

    const data = new FormData();
    data["age"]= document.getElementById("age").value;
    data["gender"] = document.getElementById("gender").value;
    params = {
        method:"POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type' :'application/json',
            "Authorization": sessionStorage.getItem("token")
        },
        body: JSON.stringify(data)
    }
    fetch(url,params)
    .then( (response) => {
    if (response.status === 200) {
        var mainContainer = document.getElementById("ShowSuccess");
            var div = document.createElement("div")
            div.innerHTML = "Profile edited successfully";
            mainContainer.appendChild(div);
        return response.json()
    } else {
        throw Error('Something went wrong ;')
    }
})
.then( (data) => {
    console.log(data)
    return data
})
.catch( (error) => {
    console.log('error',error)
})
}

// function for view profile of user
async function viewProfile(){
    console.log("calling view profile function");
    let url = 'http://localhost:8000/getuser';
    params = {
    method : 'GET',
    headers: {
      'Content-Type' : 'application/json',
      "Authorization": sessionStorage.getItem("token")
    }
    }
    try {
        let res = await fetch(url, params);
        users = JSON.stringify(await res.json())
        data = JSON.parse(users);
        console.log(data)

        var mainContainer = document.getElementById("ShowProfile");
            var div = document.createElement("div")
//            div.innerHTML = "Name: "+data["username"]+ " Password: "+data["password"]+" Joined on: "+data["date"];
               div.innerHTML = `<div class="card">
              <div class="card-body">
                <h5 class="card-title">User's Profile</h5>
                <p class="card-text">User Id : ${data.Id}</p>
                <p class="card-text">Username : ${data.Username}</p>
                <p class="card-text">Email : ${data.Email}</p>
                <p class="card-text">Age : ${data.Age}</p>
                <p class="card-text">Gender : ${data.gender}</p>
                <p class="card-text">Posts created : ${data.Posts}</p>
              </div>
            </div>`
            mainContainer.appendChild(div);

        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

// function for search by keyword (text first search )
function search_post_by_keyword(){
    console.log("calling search by keyword ");
    let url = 'http://localhost:8000/search_post';
    const data = new FormData();
    data["search_keyword"]= document.getElementById("SearchPost").value;
    params = {
        method : 'POST',
        headers: {
          'Content-Type' : 'application/json',
          "Authorization": sessionStorage.getItem("token")
        },
         body: JSON.stringify(data)
    }
    fetch(url,params)
    .then( (response) => {
    if (response.status === 200) {
        return response.json()
    }
    else if (response.status === 401 ){
        alert("There is no post related to this keyword");
    }
    else {
        throw Error('Something went wrong ;')
    }
    })
    .then( (data) => {
        posts = data["posts"];
        console.log("posts",posts)
        var mainContainer = document.getElementById("ShowSearchedPost");
        for (var i=0;i<posts.length;i++){
            var div = document.createElement("div")
            div.innerHTML = `<div class="card">
              <div class="card-body">
                <h5 class="card-title">Post ${i+1}</h5>
                <p class="card-text">User Id : ${posts[i].id}</p>
                <p class="card-text">Title : ${posts[i].title}</p>
                <p class="card-text">Content : ${posts[i].content}</p>
                <p class="card-text">User's Id  : ${posts[i].userId}</p>
              </div>
            </div>`
            mainContainer.appendChild(div);
        }
        return data
    })
    .catch( (error) => {
        console.log("error",error)
    })

}

// function for getting comments from specific boxes
function getComment(i){
    var comment = document.getElementById('comment'+i).value;
    console.log(comment)
    return comment;
}
//function for doing comment on post
function do_comment(postid,i){
    console.log("inside comment function")
    url= "http://localhost:8000/comment";
    var comment = getComment(i);
    console.log(postid, i)
    const data = new FormData();
    data["postid"] = postid
    data["comment"] = comment
    params = {
        method:"POST",
        headers: {
            'Content-Type' :'application/json',
            "Authorization": sessionStorage.getItem("token")
        },
        body: JSON.stringify(data)
    }
    fetch(url,params)
    .then( (response) => {
    if (response.status === 200) {
        console.log("successfully commented on post")
        return response.json()
    } else {
        throw Error('Something went wrong ;')
    }
})
}

