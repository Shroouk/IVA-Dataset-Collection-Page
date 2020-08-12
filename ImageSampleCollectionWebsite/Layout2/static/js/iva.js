/* global $,alert,console*/
$(function(){
  'use strict';

  $("a[href='#finish']").parent().css( "background-color", "transparent" );

  // add asterisk on required fields
  $('input').each(function(){
    if ($(this).attr('required')==='required') {
       $(this).after('<span class="asterisk">*</span>')

    }
  });

  // Hide place holder on focus
   $('[placeholder]').focus(function(){
     $(this).attr('data-text', $(this).attr('placeholder'));
     $(this).attr('placeholder', '');
   }).blur(function() {
     $(this).attr('placeholder', $(this).attr('data-text'));
   });


 // uploading photo

 const takePictureField = document.getElementById("takePictureField");
 const previewContainer = document.getElementById("imagePreview");
 const previewImage = previewContainer.querySelector(".image-preview--image");
 const inpimg = document.getElementById("inpimg");

 takePictureField.addEventListener("change", function(){
   const file =this.files[0];
   if (file){
     const reader = new FileReader();
     inpimg.style.display = "none";
     previewImage.style.display = "block";

     reader.addEventListener("load", function(){
       previewImage.setAttribute("src",this.result)
     });

     reader.readAsDataURL(file);
   }
 });




// form validation

$('#Reg').click(function(e){

var valid = this.form.checkValidity();
  if(!valid){
    Swal.fire('برجاء ملأ الحد الأدنى من الخانات!');

  }
});


});
