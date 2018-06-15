var csrftoken = $('meta[name=csrf-token]').attr('content');
function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

$(document).ready(function(){

    // Update todo
    $('#todolist li>input[type="checkbox"]').on('click', function(e){
        var todo_id = $(this).parent().closest('li').attr('id');
        $.ajax({
            url : todo_id,
            method : 'PATCH',
            data : JSON.stringify({status: $(this).prop('checked')}),
            success : function(response){
                location.reload();
            },
            error : function(error){
                console.log(error)
            }
        })
    })

    // Remove todo
    $('#todolist li>span').on('click', function(e){
        var todo_id = $(this).parent().closest('li').attr('id');
        $.ajax({
            url : todo_id,
            method : 'DELETE',
            success : function(response){
                location.reload();
            },
            error : function(error){
                console.log(error)
            }
        })
    })
})