TMP_CHATS = [];

function display(json_data) {
    clear_result();
    
    let data = JSON.parse(json_data);
    
    for (let i = 0; i < data.length; i++) {
        let item        = data[i];
        let success     = item['success'];
        let builtin     = item['builtin'];
        let type        = item['type'];
        let query       = item['query'];
        let item_data   = item['data'];

        let chat;
        if (builtin) {
            chat = new BuiltinChat(query);
        } else if (success) {
            chat = new ResultChat(query);
        } else {
            chat = new ErrorChat(query);
        }

        TMP_CHATS.push(chat);

        if (type === 'message') {
            chat.display_text(item_data);
        } else if (type === 'dataset') {
            chat.display_table(item_data);
        } else {
            console.error(item);
        }

        chat.show_buttons();
        chat.show();
    }
}

function clear_result() {
    let result = $('#result');
    result.empty();
}

