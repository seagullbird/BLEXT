var simplemde = new SimpleMDE({
    autofocus: true,
    element: $("#editor")[0],
    status: false,
    placeholder: '---\ntitle:\ncategory:\ntags: [,]\n\n---\nYour summary here.\n<!-- more -->',
    spellChecker: false,
    renderingConfig: {
        codeSyntaxHighlighting: true
    },
    tabSize: 4,
    toolbar: [{
            name: "home",
            className: "fa fa-home",
            title: "Back",
        },
        '|',
        'bold',
        'italic',
        'heading',
        '|',
        'code',
        'quote',
        'unordered-list',
        'ordered-list',
        '|',
        'link',
        'image',
        'table',
        '|',
        'preview',
        'side-by-side',
        '|', {
            name: "saveDraft",
            action: function customFunction(editor) {
                // Save draft
                if ($('#plainText').val() != '') {
                    $('#draft').val(true);
                    $('#text_form').submit();
                }
            },
            className: "fa fa-save",
            title: "Save as draft",
        }, {
            name: "publish",
            action: function customFunction(editor) {
                // Publish
                if ($('#plainText').val() != '') {
                    $('#draft').val(false);
                    $('#text_form').submit();
                }
            },
            className: "fa fa-paper-plane",
            title: "Publish",
        }
    ]
});
simplemde.toggleFullScreen();
