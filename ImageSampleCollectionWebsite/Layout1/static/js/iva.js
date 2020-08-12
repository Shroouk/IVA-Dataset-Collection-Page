// Accordion

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */
    this.classList.toggle("active");

    /* Toggle between hiding and showing the active panel */
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}

// uploading photo

const inpFile = document.getElementById("inpFile");
const previewContainer = document.getElementById("imagePreview");
const previewImage = previewContainer.querySelector(".image-preview--image");
const inpimg = document.getElementById("inpimg");
     
inpFile.addEventListener("change", function(){
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
    Swal.fire('!برجاء ملء الحد الأدنى من الخانات');
  }
});
     
