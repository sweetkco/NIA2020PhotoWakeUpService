<%inherit file="dialog.tpl"/>

<%block name="blkDialogId">diaNetworkError</%block>

<%block name="blkDialogHeader">
  Verge3D Network Operation Failed
</%block>

<%block name="blkDialogContent">
  % if type == 'NET_ERR_TIME_SKEWED':
    <div class="dialog-text">
      The difference between your local system time and the server time is too large.
      This is considered as a security issue and thus your request was denied.
    </div>
    <div class="dialog-text">
      Please correct your local system time and try again.
    </div>
  % elif type == 'NET_ERR_CANCELLED':
    <div class="dialog-text">
      Upload request cancelled.
    </div>
  % elif type == 'NET_ERR_NOTHING':
    <div class="dialog-text">
      There are no files to upload to Verge3D Network.
    </div>
  % else:
    <div class="dialog-text">
      Unknown S3 server error (${error}). Please report this issue on Verge3D forums.
    </div>
  % endif
</%block>

<%block name="blkDialogScript">
  diaNetworkErrorClose.addEventListener('click', function() { destroyDialog("diaNetworkError"); });
</%block>
