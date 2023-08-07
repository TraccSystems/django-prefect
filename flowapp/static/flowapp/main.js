let flowbtn = document.querySelector('.flowbtn');
let form = document.querySelector('.flow-form')
let container = document.querySelector('.wrapper-container')

flowbtn.addEventListener('click',showForm);


function showForm(){
    if (form.style.display === "none"){
        form.style.display = "block";
    }else{
        form.style.display = "none";
    }
}

container.addEventListener('click',(e)=>{
    if (e.target == form){
        form.style.display = 'none';
    }
})



