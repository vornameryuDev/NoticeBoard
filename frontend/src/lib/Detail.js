import { link } from "svelte-spa-router";
import Error from "../components/Error.svelte";
import fastapi from "../src/lib/api";
  

export let params = {};
let question_id = params.question_id;
let question = {question_answers:[], user:{}};

function get_detail_info() {
const url = "/api/question/detail/" + question_id;
fastapi('get', url, {},
    (json) => {question=json}
)
}  
get_detail_info();


let content = '';
let error = {detail:[]};

function postAnswer(event) {
event.preventDefault();
const url = '/api/answer/create/' + question_id;
let params = {
    'content': content
}
fastapi('post', url, params,
    (json) => {        
    get_detail_info();
    content='';
    },
    (json_error) => {
    error = json_error;
    }
)
}


