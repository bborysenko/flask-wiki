jQuery.expr[":"].contains = function( elem, i, match, array ) {
    return (elem.textContent || elem.innerText || jQuery.text( elem ) || "").toLowerCase().indexOf(match[3].toLowerCase()) >= 0;
}


function add_user(){  
    id = $(this).attr('id')
    login = $(this).attr('login');
    elem = $( '<div class="right_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', remove_user);
    $('div#dialog div.right_users_panel').append( elem );
    $(this).remove();
  }

function remove_user(){
    id = $(this).attr('id');
    login = $(this).attr('login');
    elem = $( '<div class="left_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', add_user);
    $('div#dialog div.left_users_panel').append(elem);
    $(this).remove();
  }

$(document).ready(
    function(){

        $('div#dialog div.left_users_panel > div.left_user').each(
            function(index, elem){
                $(this).bind( 'click', add_user );
            }
        );
        $('div#dialog div.right_users_panel > div.right_user').each(
            function(index, elem){
                $(this).bind( 'click', remove_user );
            }
        );
    }
);

var $dialog;
var load_users_edit = false;
$(document).ready(function(){
	$dialog_edit = $('#dialog').dialog({
                                    autoOpen: false,
                                    title: 'Права на правку',
                                    modal: true, 
                                    buttons: {
                                            "OK": function() {
                                                // очищаю содержимое тегов
                                                $('#access').tagit('removeAll');
                                                // добавляю новое содержимое
                                                $('#dialog div.right_users_panel > div.right_user').each(
                                                     function() {
                                                        login = $(this).attr('login');
                                                        name = $(this).text();
                                                        result = name;
                                                        $('#access').tagit('createTag', result);    
                                                     }
                                                );
                                                $(this).dialog('close');
                                        },
                                        "Cancel": function() {
                                            $(this).dialog("close");
                                        }
                                    }   
                                }
                            );
    $dialog_edit.dialog( "option", "width", 820 );
    $dialog_edit.dialog( "option", "height", 400 );

    // Открытие дилогового окна
    $('#add_users_edit').click(
        function (){
//            console.log('tut');
            if( !load_users_edit ){
                load_user = true;
                $('#all_users > div').each(                        
                    function(index, elem){
                        id = $(this).attr('id');
                        login = $(this).attr('login');
                        e = $( '<div class="left_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', add_user);
                        $('div#dialog div.left_users_panel').append( e );
                        $(this).bind( 'click', remove_user );                            
                    }                                                                  
                );
                
                $('div#dialog div.right_users_panel >  div.right_user').remove();
                // добавляю в правую панель выбранных пользователей 
                $('#access_edit_block li span.tagit-label').each(
                    function(){
                        name = $(this).text();
                        if(name == ""){
                            return;
                        }
                        // Поиск существующих пользователей во всех пользовтелеях
                        $('div#all_users > div:contains("' + name +  '")').each(
                            function(){
                                var id = $(this).attr('id');          
                                var login = $(this).attr('login');
                                e = $( '<div class="right_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', remove_user);
                                $('div#dialog div.right_users_panel').append(e);        
                            }
                        ); 
                    }
                );
            }
            $dialog_edit.dialog('open');
            $('div#dialog #left_panel_search').blur();
            return false; ////cancel eventbubbeling
        }
    );
});

function sravnenie_panel(){
   $('div#dialog div.right_users_panel > div.right_user').each(
       function(){        
          id = $(this).attr('id');
          $('div#dialog div.left_users_panel > div').each( 
            function(){//.remove();/*
              i = $(this).attr('id');
              if( i == id ){
                $(this).remove();
              }
            }
          );
      }
    );
}

function left_search(){
    var id = $(this).attr('id');          
    var login = $(this).attr('login');
    e = $( '<div class="left_user" id="' + id + '" login="' + login + '">' + $(this).text() + '</div>' ).bind('click', add_user);
    $('div#dialog div.left_users_panel').append(e);        
    $(this).bind( 'click', remove_user );
}

$(document).ready( function(){
   $('div#dialog #left_panel_search').keyup(
        function() {
            $('div#dialog div.left_users_panel > div').remove();
            $('div#all_users > div:contains("' + $(this).val() +  '")').each(left_search);
            sravnenie_panel();      
        }
    );
   // удалю поле ввода
//    alert(
        $('#access_edit_block li.tagit-new input').attr('readonly', 'readonly');
        $('#access_show_block li.tagit-new input').attr('readonly', 'readonly');
   //   $('#access_edit_block li.tagit-new text').prop("readonly",true);
//   $('#access_edit_block li.tagit-new').remove();
});

$(document).ready( function(){
    $("form").submit(
        function() {
            var arr_login = [];
            $('#access_edit_block li span.tagit-label').each(
                function(){
                    name = $(this).text();
                    if(name == ""){
                        return;
                    }
                    // Поиск существующих пользователей во всех пользовтелеях
                    $('div#all_users > div:contains("' + name +  '")').each(
                        function(){
                            var id = $(this).attr('id');          
                            var login = $(this).attr('login');
                            arr_login.push(login);
                        }
                    ); 
                }
            );
            $('form').css("display","none")
            $('#access').tagit('removeAll');
            for(i = 0; i < arr_login.length; i++){
                $('#access').tagit('createTag', arr_login[i]);
            }
        }
    );
});
$(document).ready(                                                             
    function(){                                             
        $('#all_users').prepend('<div id="-1" login="all"><div class="user_data">All</div></div>');
// произвожу замену имени         
        var arr_name = [];
        $('#access_edit_block li span.tagit-label').each(
            function(){
                login = $(this).text();
                if(login == ""){
                    return;
                }
                // Поиск существующих пользователей во всех пользовтелеях
                $('div#all_users > div').each(
                    function(){
                        var id = $(this).attr('id');          
                        l = $(this).attr('login');
                        if( l != login ){
                            return;
                        }
                        var name = $(this).text();
                        arr_name.push(name);
                    }
                ); 
            }
        );
        
        $('#access').tagit('removeAll');
        for(i = 0; i < arr_name.length; i++){
            $('#access').tagit('createTag', arr_name[i]);
        }
        
        var text = "Поиск...";
        $('.ui-dialog-titlebar').focus();
        $('div#dialog #left_panel_search').val(text);
        $('div#dialog #left_panel_search').focus(
            function(){
                $(this).addClass("active");
                if($(this).attr("value") == text){
                    $(this).attr("value", "");
                }
            }
        );
        $('div#dialog #left_panel_search').blur(
            function(){
                $(this).removeClass("active");
                if($(this).attr("value") == "") $(this).attr("value", text);
            }
        );
    }                                                                                                                                        
) ; 
