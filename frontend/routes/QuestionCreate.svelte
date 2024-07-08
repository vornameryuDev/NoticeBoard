<script>
    import { push } from 'svelte-spa-router';
    import Error from "../components/Error.svelte";
    import fastapi from '../src/lib/api';

    let error = {detail:[]};
    let subject = '';
    let content = '';
    
    function postQuestion(event) {
        event.preventDefault();
        let url = "/api/question/create";
        let params = {
            subject: subject,
            content: content
        }
        fastapi('post', url, params, 
            (json) => {
                push('/');
            },
            (json_error) => {
                error = json_error;
            }
        )
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문등록</h5>

    <Error error={error} />

    <form method="post">
        <div class="mb-3">
            <label for="subject">제목</label>
            <input type="text" class="form-control" id="qc-subject" bind:value="{subject}">
            <label for="content">내용</label>
            <textarea rows="15" id='qc-content' class="form-control" bind:value={content}></textarea>
        </div>
        <button type="submit" class="btn btn-primary" on:click="{postQuestion}">
            생성하기
        </button>
</div>
