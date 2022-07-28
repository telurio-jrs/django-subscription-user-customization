// beneficiaries labels "View Details", "Edit" and "Delete"
$(document).on('click', '.article_del', function() {
    $('#del_article').val($(this).data('value'));
});
