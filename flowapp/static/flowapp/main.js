let connection = document.querySelector('.connections');
let tabs = document.querySelectorAll('.formtabs');
let connection_btn = document.querySelector('.connection_btn');
let connections_form_container = document.querySelector('.connections-form-container');
let page_content = document.querySelector('.page-content');

connection_btn.addEventListener('click',()=>{
   connections_form_container.style.transition ="linear 110s"
   connections_form_container.style.display ="block"

})




connection.addEventListener('input',(e)=>{
   for(let index=0; index < tabs.length; index++)
   if(e.target.value ==="S3"){
      tabs[0].style.display= "block";
      tabs[1].style.display= "none";
      tabs[2].style.display= "none";
      tabs[3].style.display= "none";
   }else if(e.target.value ==="Postgress"){
      tabs[1].style.display= "block";
      tabs[0].style.display= "none";
      tabs[2].style.display= "none";
      tabs[3].style.display= "none";
   }else if(e.target.value ==="Pinecone"){
      tabs[1].style.display= "none";
      tabs[0].style.display= "none";
      tabs[2].style.display= "block";
      tabs[3].style.display= "none";
   }else if(e.target.value ==="SingleStore"){
      tabs[1].style.display= "none";
      tabs[0].style.display= "none";
      tabs[2].style.display= "none";
      tabs[3].style.display= "block";
   }

})







