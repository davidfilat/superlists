window.Superlists = {};
window.Superlists.initialize = function () {
    u('input[name="text"]').on('keypress', function () {
        u('.text-danger').attr({style: 'display:none;'});
    });
}