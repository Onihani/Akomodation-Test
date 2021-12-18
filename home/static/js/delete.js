var id = $("#delete").attr("data-catid")

$("#delete").click( (e) => {
    $.ajax({type: 'GET', url: 'account/delete/' + id, data: {pk: id}, success: (data) => {
        $("#delete").text("deleted")
    }, error: (error) =>{
        $("#delete").text("error")
    }})
})
