
var videoEreaStatic = false;
var videoEditArea = $('#edit-area')
var table = $('#table-t')


$('#open-add-video-btn').click(function () {
    if (!videoEreaStatic){
        videoEditArea.show();
        table.hide();
        videoEreaStatic = true;
    }
    else {
        videoEditArea.hide();
        table.show();
        videoEreaStatic = false;
    }
})