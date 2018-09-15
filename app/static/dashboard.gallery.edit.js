
$( document ).ready(function() {
  $("#edit_gallery").click(function(event) {
      $("p.success").remove();
      $("p.fail").remove();
      $("#form_edit_gallery").ajaxSubmit({
          url:$SCRIPT_ROOT + $data["api_endpoints"]["edit_gallery"],
          success: function(data) {
            if (data.success) {
              flash = $("<p class='success'></p>").text(data.university_name + " " + $L["add_success"])
            } else {
              flash = $("<p class='fail'></p>").text(data.err)
            }
            flash.insertBefore($("button#edit_gallery"))
          }
        });
      return false;
  });

  $("div#dropzone").dropzone({
    url: $data["image_upload_url"],
    addRemoveLinks: true,
    autoProcessQueue: false,

    init: function () {
      var this_dropzone = this;

      this_dropzone.on("processing", function() {
        this_dropzone.options.autoProcessQueue = true;
      });

      this_dropzone.on("queuecomplete", function() {
        this_dropzone.getFilesWithStatus("existing").forEach (function (f) {
          alert("Need to pull " + f.name + " into pending");
        });
      });

      $("#edit_gallery_submit").click(function (e) {
        e.preventDefault();
        this_dropzone.processQueue();
      });

      $data["existing_images"].forEach(function(img) {
        var mockFile = { name: img.name, size: img.size, status:"existing"};
        this_dropzone.options.addedfile.call(this_dropzone, mockFile);
        this_dropzone.options.thumbnail.call(this_dropzone, mockFile, img.thumb_url);
        this_dropzone.files.push(mockFile);
      });
    },

    removedfile: function(file) {
      var name = file.name;        
      return (_ref = file.previewElement) != null ? _ref.parentNode.removeChild(file.previewElement) : void 0;
    },
  });

  $("div#dropzone").sortable({
    items:'.dz-preview',
    cursor: 'move',
    opacity: 0.5,
    containment: 'div#dropzone',
    distance: 20,
    tolerance: 'pointer'
  });
});
