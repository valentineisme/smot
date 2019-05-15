//
//pesquisas
//

function estado_cidade() {
    if ($("select#bh").val() == 'selecione') {
        var options = '<option>Selecione primeiro uma bacia hidrográica</option>';
        $("select#rio").html(options);
        $("select#rio").attr('disabled', true);
        var options = '<option>Selecione primeiro um rio</option>';
        $("select#ponto_monitoramento").html(options);
        $("select#ponto_monitoramento").attr('disabled', true);
        var options = '<option>Selecione primeiro um ponto de monitoramento</option>';
        $("select#coleta").html(options);
        $("select#coleta").attr('disabled', true);
    } else {
        $.ajax({
            type: 'GET',
            url: '/ajax/pesquisa/',
            data: {
                bh: $("select#bh").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            success: function (data) {
                var options = '<option>Selecione um rio</option>';
                for (var i = 0; i < data.length; i++) {
                    options += '<option value="' + data[i].pk + '">' + data[i].fields['nome'] + '</option>';
                }
                $("select#rio").html(options);
                $("select#rio").attr('disabled', false);
            },
            error: function (xhr, errmsg) {
                console.log(xhr.status + ": " + xhr.responseText + "Error: " + errmsg);
            }
        });
    }
}

