<%inherit file="dialog.tpl"/>

<%block name="blkDialogId">diaError</%block>

<%block name="blkDialogHeader">
  Operation Failed
</%block>

<%block name="blkDialogContent">
  <div class="dialog-text">
    ${message}
  </div>
  <button id="diaErrorOk" class="button">Got it!</button>
</%block>

<%block name="blkDialogScript">
  diaErrorClose.addEventListener('click', function() { destroyDialog("diaError"); });
  diaErrorOk.addEventListener('click', function() { destroyDialog("diaError"); });

  focusElem('diaErrorOk');
</%block>
