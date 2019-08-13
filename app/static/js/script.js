$(".nav .nav-link").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).addClass("active");
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#img-upload').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$('#validatedCustomFile').on('change',function(){
				var input = $(this);
                //get the file name
                var fileName = $(this).val();
                fileName = fileName.toString().replace(/\\/g, '/').replace(/.*\//, '');
                //replace the "Choose a file" label
                //label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
                $(this).next('.custom-file-label').html(fileName);
		        readURL(this)
            })