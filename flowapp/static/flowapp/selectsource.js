let s3sourceform = document.querySelector('.s3Source')
let pygonsourceForm = document.querySelector('.postgress')
let selectsource = document.querySelector('.source')



selectsource.addEventListener('input',(e)=>{
    if(e.target.value === "AWS"){
        s3sourceform.style.display ="block";
        pygonsourceForm.style.display ="none";
    }else if(e.target.value === "postgress"){
         s3sourceform.style.display ="none";
        pygonsourceForm.style.display ="block";

    }else if(e.target.value === "Select"){
         s3sourceform.style.display ="none";
        pygonsourceForm.style.display ="none";

    }
})