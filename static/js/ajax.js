//imagem
var id_cache = '';
function monitoramento_imagem(id) {
    $("input#imagem").attr('value', id);
    $("span#corner" + id).html('<a class="ui left teal corner label"><i class="checkmark icon"></i></a><input type="hidden" name="imagem_selecionada" value="'+id+'">');
    if (id_cache != '') {
        $("span#corner" + id_cache).html('');
    }
    id_cache = id;
}

//ativar campos
function ativar() {
    $('button.botaoProximo').removeAttr('disabled');
}

// function valida_form() {
//     if (document.getElementById("id_objeto1").value == "Floresta") {
//         alert('Por favor, preencha o campo nome');
//         document.getElementById("id_objeto1").focus();
//         return false
//     }
// }

//comunidade
function comu_editar(id) {
    $.ajax({
        type: 'GET',
        url: '/Comunidade/Edit_Campos/',
        data: {
            comu: id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        success: function (data) {
            $("input#nome_comu").attr('value', data[0].fields['nome']);
            $("input#bairro_comu").attr('value', data[0].fields['bairro']);
            $("input#cidade_comu").attr('value', data[0].fields['cidade']);
            $("input#estado_comu").attr('value', data[0].fields['estado']);
            $("input#id_comu").attr('value', data[0].pk);
        },
        error: function (xhr, errmsg) {
            console.log(xhr.status + ": " + xhr.responseText + "Error: " + errmsg);
        }
    });
}

function comu_excluir(id) {
    var nome = $("input#" + id).val();
    $("span#nome").html(nome);
    var link = 'Delete/' + id;
    $("a#link").attr('href', link);
}

function imagem_excluir(id, comu_id) {
    var nome = $("input#" + id).val();
    $("span#nome").html(nome);
    var link = '/Imagem_Lista/Delete/' + id + '/' + comu_id;
    $("a#link").attr('href', link);
}

function historico_excluir(id, imagem_id, comunidade_id) {
    var nome = $("input#" + id).val();
    $("span#nome").html(nome);
    var link = '/Historico/Delete/' + id + '/' + imagem_id + '/' + comunidade_id;
    $("a#link").attr('href', link);
}

function mostrar_conteudo(){
    $('div.modalListarImagem').removeClass('modal')
}
