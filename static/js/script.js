$(document).ready(function () {
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
        $('.modalCadastro').modal('show');
    });
});