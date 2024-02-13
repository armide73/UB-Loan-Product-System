$(document).ready(function() {

    $("#my-form").on("submit", function(event) {
        event.preventDefault();
      });

    // When the user clicks on the button, open the file chooser dialog
    $("#update-profile-picture").click(function() {
      var fileInput = document.getElementById("file-input");
      fileInput.click();
    });
  
    // When the user selects a file, send it to the Flask endpoint
    $("#file-input").change(function() {
      var file = this.files[0];
      var formData = new FormData();
      formData.append("file", file);
  
      $.ajax({
        url: "administration_profile_picture",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          // Update the profile picture
        //   $("#profile-picture").attr("src", response.data.url);
        console.log(response)
            location.reload();
        },
        error: function(error) {
            // Handle the error
            console.log(error)
            location.reload();
        }
      });
    });
  });