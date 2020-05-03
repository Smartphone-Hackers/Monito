var programming = document.getElementById('id_program_lang').addEventListener('click', showTopics);
var topics = document.getElementById('id_topic');

function showTopics(e){
    var getlanguage = e.target.value;
    if (getlanguage === 'python'){
        var python_topics = ['lists', 'tuples', 'dictionaries', 'sets'];
        topics.textContent = "";
        python_topics.forEach(function(topic){
            var option_tag = document.createElement('option');
            option_tag.value = topic;
            option_tag.append(document.createTextNode(topic));
            topics.appendChild(option_tag);
        });
    } else if(getlanguage === 'oracle'){
        var oracle_topics = ['selection', 'restriction & sorting', 'ddl', 'dml'];
        topics.textContent = "";
        oracle_topics.forEach(function(topic){
            var option_tag = document.createElement('option');
            option_tag.value = topic;
            option_tag.append(document.createTextNode(topic));
            topics.appendChild(option_tag);
        }); 
    } else if(getlanguage === 'java'){
        var java_topics = ['class & objects', 'polymorphism', 'inheritance'];
        topics.textContent = "";
        java_topics.forEach(function(topic){
            var option_tag = document.createElement('option');
            option_tag.value = topic;
            option_tag.append(document.createTextNode(topic));
            topics.appendChild(option_tag);
        });
    }
};