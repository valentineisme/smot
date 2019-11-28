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
            $("input#cidade_cad").attr('value', data[0].fields['cidade']);
            $("input#estado_comu").attr('value', data[0].fields['estado']);
            $("input#estado_cad").attr('value', data[0].fields['estado']);
            $("input#id_comu").attr('value', data[0].pk);
        },
        error: function (xhr, errmsg) {
            console.log(xhr.status + ": " + xhr.responseText + "Error: " + errmsg);
        }
    });
}

function comu_excluir(id, page) {
    var nome = $("input#" + id).val();
    $("span#nome_exc").html(nome);
    var link = 'Delete/' + id + '/' + page;
    $("a#link_exc").attr('href', link);
}

//imagem
function imagem_pub() {
    if ($('input[name=data_imagem]')) {
        $.ajax({
            type: 'GET',
            url: '/Imagem_Publica/',
            data: {
                dataImagem: $('input[name=data_imagem]').val(),
                comu: $('input[name=comu_id]').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            success: function (data) {
                var option = "<option value=''>Latitude - Longitude</option>";
                var options = "";
                $("select#coor").html(option);
                $("select#coor").removeAttr('disabled');

                for (var i = 0; i < data.length; i++) {
                    if (data[i] !== '') {
                        option += "<option value='" + data[i].pk + "'>" + data[i].fields['latitude'] + " - " + data[i].fields['longitude'] + "</option>";
                        options = 'a';
                        cards = "selecione uma coordenada";
                    }
                }

                if (options === '') {
                    option = "<option value=''>nenhuma coordenada</option>";
                    cards = "nenhuma imagem relacionada para essa data";
                }
                $("select#coor").html(option);
                // $("select#coor").html(options);
                $("article#div_img").html(cards);
            },
            error: function (xhr, errmsg) {
                console.log(xhr.status + ": " + xhr.responseText + "Error: " + errmsg);
            }
        });
    }
}

function imagem_pub_coor() {
    if ($('select[name=coor]')){
        $.ajax({
            type: 'GET',
            url: '/Imagem_Publica/',
            data: {
                img: $('select[name=coor]').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            success: function (data) {
                var cards = "";
                for (var i = 0; i < data.length; i++) {
                    if (data[i] !== '') {
                        cards += "<div class='ui card'><div class='image'><img id='url_imagem' src='/media/" + data[i].fields['img'] + "'/></div>" +
                            "<div class='content'><a class='header' id='data_imagem'>" + data[i].fields['dataImagem'] + "</a>" +
                            "<div class='item' id='lati'>" + data[i].fields['latitude'] + "</div><div class='item' id='longi'>" + data[i].fields['longitude'] + "</div><div class='ui divided list'>" +
                            "<a class='cursorPointer utilizarImagem ui-tooltip' data-tooltip='Utilizar' onclick='utilizar("+ data[i].pk + ")'><i class='ui download green large icon'></i>" +
                            "</a></div></div></div>";
                    }
                }
                if (cards === '') {
                    cards = "nenhuma imagem relacionada para essa coordenada";
                }
                $("article#div_img").html(cards);
            },
            error: function (xhr, errmsg) {
                console.log(xhr.status + ": " + xhr.responseText + "Error: " + errmsg);
            }
        });
    }
}

function imagem_editar(id) {
    $.ajax({
        type: 'GET',
        url: '/Imagem_Lista/Edit_Campos/',
        data: {
            img: id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        success: function (data) {
            $("input#data_img").attr('value', data[0].fields['dataImagem']);
            $("input#lati_img").attr('value', data[0].fields['latitude']);
            $("input#longi_img").attr('value', data[0].fields['longitude']);
            $("input#id_imagem").attr('value', data[0].pk);
        },
        error: function (xhr, errmsg) {
            console.log(xhr.status + ": " + xhr.responseText + "Error: " + errmsg);
        }
    });
}

function imagem_excluir(id, comu_id, page) {
    var nome = $("input#" + id).val();
    $("span#nome").html(nome);
    var link = '/Imagem_Lista/Delete/' + id + '/' + comu_id + '/' + page;
    $("a#link").attr('href', link);
}


//historico
function historico_excluir(id, imagem_id, comunidade_id, page) {
    var nome = $("input#" + id).val();
    $("span#nome").html(nome);
    var link = '/Historico/Delete/' + id + '/' + imagem_id + '/' + comunidade_id + '/' + page;
    $("a#link").attr('href', link);
}

function historico_excluir_lati(id, imagem_id, comunidade_id, page) {
    var nome = $("input#" + id).val();
    $("span#nome").html(nome);
    var link = '/Historico/Delete/Lati/' + id + '/' + imagem_id + '/' + comunidade_id + '/' + page;
    $("a#link").attr('href', link);
}

//caso
function caso_editar(id) {
    $.ajax({
        type: 'GET',
        url: '/Casos/Edit_Campos/',
        data: {
            caso: id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        success: function (data) {
            $("input#ob1").attr('value', data[0].fields['objeto1']);
            $("input#rel").attr('value', data[0].fields['relacao']);
            $("input#ob2").attr('value', data[0].fields['objeto2']);
            $("input#id_distancia").attr('value', data[0].fields['distancia']);
            $("input#restri").attr('value', data[0].fields['restricao']);
            $("input#id_resultado").attr('value', data[0].fields['resultado']);
            $("input#id_plano_acao").attr('value', data[0].fields['plano_acao']);
            $("input#caso_id").attr('value', data[0].pk);
        },
        error: function (xhr, errmsg) {
            console.log(xhr.status + ": " + xhr.responseText + "Error: " + errmsg);
        }
    });
}

function caso_excluir(caso_id, ob1_id, rel_id, ob2_id) {
    var nome = $("input#" + caso_id).val();
    $("span#nome").html(nome);
    var link = '/Casos/Delete/' + caso_id + '/' + ob1_id + '/' + rel_id + '/' + ob2_id;
    $("a#link").attr('href', link);
}

function mostrar_conteudo(){
    $('div.modalListarImagem').removeClass('modal')
}

function permitir(id, page) {
    var links = 'Permitir/' + id + '/' + page;
    $("a#link_per").attr('href', links);
}

function utilizar(id) {
    var links = 'Utilizar/' + id;
    $("a#link_uti").attr('href', links);
}

// //data_nascimento
// function VerificaData() {
//     if (validardataDeNascimento(document.imagem_form.data.value)) {
//         document.getElementById("msgdata").innerHTML = "";
//
//     } else {
//         errors = "1";
//         document.getElementById("msgdata").innerHTML = "<font color='red'>Data Invalida </font>";
//         document.retorno = (errors == '');
//     }
// }
//
// function validardataDeNascimento(data) {
//
//     dataAtual = new Date();
//     data = new Date(data);
//     if ((data < dataAtual)){
//         console.log("Data Válida");
//         return true;
//     } else {
//         console.log("Data Inválida");
//         return false;
//     }
// }

//email

function VerificaEmail() {
    if (validacaoEmail(document.usuario_form.email.value)) {
        document.getElementById("msgemail").innerHTML = "";
         document.usuario_form.submit();
    } else {
        errors = "1";
        document.getElementById("msgemail").innerHTML = "<font color='red'>E-mail invalido </font>";
        document.retorno = (errors == '');
    }
}

function validacaoEmail(email) {
    usuario = email.substring(0, email.indexOf("@"));
    dominio = email.substring(email.indexOf("@") + 1, email.length);

    if ((usuario.length >= 1) &&
        (dominio.length >= 3) &&
        (usuario.search("@") == -1) &&
        (dominio.search("@") == -1) &&
        (usuario.search(" ") == -1) &&
        (dominio.search(" ") == -1) &&
        (dominio.search(".") != -1) &&
        (dominio.indexOf(".") >= 1) &&
        (dominio.lastIndexOf(".") < dominio.length - 1)) {
        return true;
    } else {
        return false;
    }
}
