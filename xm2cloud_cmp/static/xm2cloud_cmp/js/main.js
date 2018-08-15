$._default = function (options, k, _default) {
    if(k in options){
        return options[k];
    }
    return _default;
};

$._message = function (options) {
    options = options || {};
    var msg = $._default(options, 'msg', '');
    options.error_title = $._default(options, 'error_title', '错误');
    options.error_width = $._default(options, 'error_width', 500);
    options.error_height = $._default(options, 'error_height', 'auto');
    options.error_timeout = $._default(options, 'error_timeout', 0);

    $.messager.show({
        msg: msg,
        title: options.error_title,
        width: options.error_width,
        height: options.error_height,
        style:{right: '', bottom: ''},
        timeout: options.error_timeout
    });
};

$._ajax = function (options) {
    options = options || {};
    options.type = $._default(options, 'type', 'POST');
    options.async = $._default(options, 'async', true);
    options.dataType = $._default(options, 'dataType', 'json');
    options.error = $._default(options, 'error', function (jqXHR, textStatus, errorThrown) {
        var err = {__all__: []};
        if(jqXHR.status == 0){
            err.__all__.push('Unknown network error.');
        }
        if(jqXHR.status == 500){
            err.__all__.push('Unknown server error.');
        }
        if(err.__all__.length > 0){
            jqXHR.responseText = JSON.stringify(err);
        }
        options.msg = '<div class="error-msg">'
                    + '<p>状态文本: <span class="font-grey">'+textStatus+'</span></p>'
                    + '<p>状态代码: <span class="font-grey">'+jqXHR.status+'</span></p>'
                    + '<p>响应文本: <span class="font-grey">'+jqXHR.responseText+'</span></p>'
                    + '</div>';
        $._message(options);
    });
    $.ajax(options);
};

$._control = function(p, options){
    options = options || {};
    options.cache = $._default(options, 'cache', false);
    options.method = $._default(options, 'method', 'GET');
    options.dataType = $._default(options, 'dataType', 'json');
    options.queryParams = $._default(options, 'queryParams', {});
    options.onBeforeLoad = $._default(options, 'onBeforeLoad', function () {
        $(this).panel('clear');
    });
    $(p).panel(options);
};

$._datagrid = function (p, options) {
    options = options || {};
    options.fit = $._default(options, 'fit', true);
    options.method = $._default(options, 'method', 'GET');
    options.pageSize = $._default(options, 'pageSize', 20);
    options.striped = $._default(options, 'striped', false);
    options.remoteSort = $._default(options, 'remoteSort', false);
    options.rownumbers = $._default(options, 'rownumbers', true);
    options.pagination = $._default(options, 'pagination', true);
    options.fitColumns = $._default(options, 'fitColumns', true);
    options.singleSelect = $._default(options, 'singleSelect', true);
    options.checkOnSelect = $._default(options, 'checkOnSelect', true);
    options.selectOnCheck = $._default(options, 'selectOnCheck', true);

    $(p).datagrid(options);
};

$._window = function (p, options) {
    options = options || {};
    options.width = $._default(options, 'width', '50%');
    options.height = $._default(options, 'height', 350);
    options.closed = $._default(options, 'closed', false);
    options.closable = $._default(options, 'closable', true);
    options.collapsible = $._default(options, 'collapsible', false);
    options.minimizable = $._default(options, 'minimizable', false);
    options.maximizable = $._default(options, 'maximizable', true);

    options.onResize = $._default(options, 'onResize', function (width, height) {
        $(this).window('center');
    });

    $(p).window(options);
};

$._combobox = function (p, options) {
    options = options || {};
    options.reversed = $._default(options,  'reversed', false);
    options.valueField = $._default(options, 'valueField', 'id');
    options.textField = $._default(options, 'textField', 'name');
    options.panelHeight = $._default(options, 'panelHeight', 'auto');
    options.selectOnNavigation = $._default(options, 'selectOnNavigation', true);
    options.formatter = $._default(options, 'formatter', function (row) {
        return '<span>'+row.name+'</span><br/><span style="color:#888">'+row.notes +'</span>';
    });

    $(p).combobox(options);
};

$._editor = function (p, options) {
    options = options || {};
    options.contents = $._default(options, 'contents', '');
    options.folding = $._default(options, 'folding', true);
    options.theme = $._default(options, 'theme', 'github');
    options.language = $._default(options, 'language', 'sh');
    options.readonly = $._default(options, 'readonly', false);

    var editor = ace.edit(p);
    editor.setReadOnly(options.readonly);
    editor.setAutoScrollEditorIntoView(true);

    editor.setTheme('ace/theme/'+options.theme);
    editor.getSession().setUseWrapMode(options.folding);
    if(options.contents) editor.setValue(options.contents);
    editor.getSession().setMode('ace/mode/'+options.language);

    editor.setOptions({
        enableSnippets: true,
        enableLiveAutocompletion: true,
        enableBasicAutocompletion: true
    });


    return editor;
};

$._render = function (p, options) {
    var chart = echarts.init(document.getElementById(p));
    options = options || {};

    chart.setOption(options);

    return chart
};

