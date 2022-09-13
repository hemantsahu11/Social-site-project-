console.log("this is javascript file ");

function getdata(){
    console.log("calling getdata");
    url = "http://localhost:8000/home";
    fetch(url).then((response)=> {
        console.log("Inside first then")
        return response.json();
    }).then((data)=> {
        console.log("Inside second then ")
        console.log(data)
    })
}

getdata()

