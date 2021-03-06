$(document).ready(function () {

    $('.menu .item')
        .tab()
    ;

    //cadastro
    $("body").on("click", ".cadastrarUsuario", function () {
        $('.modalCadUser').modal('show');
    });
    $("body").on("click", ".logar", function () {
        $('.modalLogar').modal('show');
    });
    $("body").on("click", ".verSobre", function () {
        $('.modalSobre').modal('show');
    });

    //comunidade
    $("body").on("click", ".verHistorico", function () {
        $('.modalListarComu').modal('show');
    });
    $("body").on("click", ".adicionarComu", function () {
        $('.modalFormComunidade').modal('show');
    });
    $("body").on("click", ".editarComu", function () {
        $('.modalEditarComunidade').modal('show');
    });
    $("body").on("click", ".excluirComu", function () {
        $('.modalExcluirComunidade').modal('show');
    });
    $("body").on("click", ".permitirComu", function () {
        $('.modalPermitir').modal('show');
    });
    $("body").on("click", ".utilizarComu", function () {
        $('.modalUtilizar').modal('show');
    });

    //imagem
    $("body").on("click", ".adicionarImagem", function () {
        $('.modalCadImagem').modal('show');
    });
    $("body").on("click", ".ExcluirImagem", function () {
        $('.modalExcluirImagem').modal('show');
    });
    $("body").on("click", ".PermitirImagem", function () {
        $('.modalPermitir').modal('show');
    });
    $("body").on("click", ".editarImagem", function () {
        $('.modalEditarImagem').modal('show');
    });
    $("body").on("click", ".utilizarImagem", function () {
        $('.modalUtilizar').modal('show');
    });

    //caso
    $("body").on("click", ".cadCaso", function () {
        $('.modalFormCaso').modal('show');
    });
    $("body").on("click", ".excluirCaso", function () {
        $('.modalExcluirCaso').modal('show');
    });
    $("body").on("click", ".editarCaso", function () {
        $('.modalEditarCaso').modal('show');
    });

    //hist
    $("body").on("click", ".excluirHist", function () {
        $('.modalExcluirHist').modal('show');
    });
    // $("body").on("click", ".abrirDetalhesHist", function () {
    //     $('.modalDetalhes').modal('show');
    // });

    //tabelas de pesquisa
    var filtro = document.getElementById('filtro_pesquisa');
    var tabela = document.getElementById('tabela_lista1');
    filtro.onkeyup = function () {
        var nomeFiltro = filtro.value;
        for (var i = 1; i < tabela.rows.length; i++) {
            var conteudoCelula = tabela.rows[i].cells[0].innerText.toLocaleLowerCase();
            var corresponde = conteudoCelula.indexOf(nomeFiltro) >= 0;
            tabela.rows[i].style.display = corresponde ? '' : 'none';
        }
    };

    var filtro2 = document.getElementById('filtro_pesquisa2');
    var tabela2 = document.getElementById('tabela_lista2');
    filtro2.onkeyup = function () {
        var nomeFiltro = filtro2.value;
        for (var i = 1; i < tabela2.rows.length; i++) {
            var conteudoCelula = tabela2.rows[i].cells[0].innerText.toLocaleLowerCase();
            var corresponde = conteudoCelula.indexOf(nomeFiltro) >= 0;
            tabela2.rows[i].style.display = corresponde ? '' : 'none';
        }
    };

    $(".esquerda.logo_centro_smot").mouseenter(function () {

        var img_smot = $('.logo_centro_smot');

        $({rotation: 0}).animate({rotation: 1080}, {
            duration: 5000,
            easing: 'linear',
            step: function () {
                img_smot.css({transform: 'rotate(' + this.rotation + 'deg)'});
                console.log(this.rotation);
            }
        });
    });

    $(".direita.logo_centro_magna").mouseenter(function () {

        var img = $('.logo_centro_magna');

        $({rotation: 0}).animate({rotation: 1080}, {
            duration: 5000,
            easing: 'linear',
            step: function () {
                img.css({transform: 'rotate(' + this.rotation + 'deg)'});
                console.log(this.rotation);
            }
        });
    });

});
