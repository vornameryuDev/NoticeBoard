<script>
    import { push } from 'svelte-spa-router';
    import Error from "../components/Error.svelte";
    import fastapi from '../src/lib/api';

    export let params = {};
    let question_id = params.question_id;
    console.log(question_id);

    let error = {detail:[]};
    let subject = '';
    let content = '';


    fastapi('get', '/api/question/detail/' + question_id, {},
        (json) => {
            subject = json.subject;
            content = json.content;
        }
    )
    
    function modifyQuestion(event) {
        event.preventDefault()
        let url = "/api/question/update";
        let params = {
            question_id: question_id,
            subject: subject,
            content: content,
        }
        fastapi('put', url, params, 
            (json) => {
                push('/detail/'+question_id);
            }
        )
    }

</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문수정</h5>

    <!-- <Error error={error} /> -->

    <form method="post">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" id="qc-subject" bind:value="{subject}">
            <label for="content">내용</label>
            <textarea rows="15" id='qc-content' class="form-control" bind:value={content}></textarea>
        </div>
        <button type="submit" class="btn btn-primary" on:click="{modifyQuestion}">
            수정하기
        </button>
</div>
