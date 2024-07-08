<script>
    import { push } from 'svelte-spa-router';
    import Error from "../components/Error.svelte";
    import fastapi from '../src/lib/api';
    import { is_login } from '../src/lib/store';
    

    export let params = {};
    let answer_id = params.answer_id;
    let error = {detail:[]};
    let subject = '';
    let content = '';
    let answer = {};
    let question_id = 0;


    fastapi('get', '/api/answer/detail/' + answer_id, {},
        (json) => {               
            content = json.content;
            question_id=json.question_id;            
        }
    )
    
    function modifyAnswer(event) {
        event.preventDefault();
        const url = "/api/answer/update";
        let params = {
            answer_id:answer_id,
            content:content
        }
        fastapi('put', url, params,
            (json) => {
                push('/detail/' + question_id);
            },
            (json_error) => {
                error = json_error;
            }
        )
        
    }

</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">답변수정</h5>

    <Error error={error} />

    <form method="post">
        <div class="mb-3">            
            <label for="content">내용</label>
            <textarea rows="15" id='qc-content' class="form-control" bind:value={content}></textarea>
        </div>
    </form>

    {#if $is_login}
    <button type="submit" class="btn btn-primary" on:click="{modifyAnswer}">
        수정하기
    </button>        
    {/if}
</div>
