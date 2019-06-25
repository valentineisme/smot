$(document).ready(function () {

    var filtro = document.getElementById('filtro_pesquisa');
    var tabela = document.getElementById('tabela_lista');
    filtro.onkeyup = function () {
        var nomeFiltro = filtro.value;
        for (var i = 1; i < tabela.rows.length; i++) {
            var conteudoCelula = tabela.rows[i].cells[0].innerText;
            var corresponde = conteudoCelula.indexOf(nomeFiltro) >= 0;
            tabela.rows[i].style.display = corresponde ? '' : 'none';
        }
    };


    $("#owl-homepage").owlCarousel({

        autoPlay: false, //Set AutoPlay to 3 seconds
        items: 3,
        itemsDesktop: [1199, 3],
        itemsDesktopSmall: [979, 3],
        navigation: true,
        navigationText: ["voltar", "próximo"],
        autoHeight: false,


    });


    $('.ui.dropdown')
        .dropdown()
    ;

    $('.ui.checkbox')
        .checkbox()
    ;


    var $section = $('section').first();
    $section.find('.panzoom').panzoom({
        $zoomIn: $section.find(".zoom-in"),
        $zoomOut: $section.find(".zoom-out"),
        $zoomRange: $section.find(".zoom-range"),
        $reset: $section.find(".reset")
    });


    $('#range-1').range({
        min: 0,
        max: 100,
        start: 0,
    });

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

    //imagem
    $("body").on("click", ".adicionarImagem", function () {
        $('.modalCadImagem').modal('show');
    });
    $("body").on("click", ".ExcluirImagem", function () {
        $('.modalExcluirImagem').modal('show');
    });

    //caso
    $("body").on("click", ".cadCaso", function () {
        $('.modalFormCaso').modal('show');
    });

    //hist
    $("body").on("click", ".excluirHist", function () {
        $('.modalExcluirHist').modal('show');
    });
});