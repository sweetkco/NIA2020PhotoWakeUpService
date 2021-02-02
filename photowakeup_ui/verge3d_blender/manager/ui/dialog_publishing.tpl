<%inherit file="dialog.tpl"/>

<%block name="blkDialogId">diaPublishing</%block>

<%block name="blkDialogHeader">
  Publishing Application on Verge3D Network...
</%block>

<%block name="blkDialogContent">

  <div class="publishing-preloader-cont">
    <div class="publishing-percentage" id='publishingPercentage'>0%</div>
    <div class="publishing-preloader"></div>
  </div>

  <button class="button" id="stopUploading">Cancel</button>
  
</%block>

<%block name="blkDialogScript">
  ${parent.blkDialogScript()}

  stopUploading.addEventListener('click', function(event) {
      makeRequest('/storage/net/?req=cancel', null, null);
  });
</%block>

