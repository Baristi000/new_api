fetch("localhost:8000/login/token",{
    method:"POST",
    body:{
        username:"1",
        password:"sdas"
    }
}).then(res =>{
    console.log(res)
})
