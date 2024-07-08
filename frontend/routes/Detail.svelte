<script>
  
  import { link } from "svelte-spa-router";
  import Error from "../components/Error.svelte";
  import fastapi from "../src/lib/api";
  import { username, is_login } from "../src/lib/store";
  import {push} from "svelte-spa-router";
  

  export let params = {};
  let question_id = params.question_id;
  let question = {question_answers:[], user:{}, voter:[]};

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
      content: content
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

  //question vote
  function questionVote(question_id) {
    const url = '/api/question/vote';
    let params = {
      question_id: question_id,      
    }

    fastapi('post', url, params, 
      get_detail_info(),
      (json_error) => {error=json_error}
    );
  }

  //answer vote
  function answerVote(answer_id){
    console.log('vote');
    const url = '/api/answer/vote';
    let params = {
      answer_id:answer_id
    }
    fastapi('post', url, params,
      get_detail_info(),
      (json_error) => {error=json_error}
    )
  }

  //question Delete
  function questionDel(question_id) {
    console.log('delete');
    const url = '/api/question/delete'
    let params = {
      question_id:question_id
    }
    fastapi("delete", url, params, push('/'), (error_json) => {error=error_json})
  }

  //answer Delete
  function answerDel(answer_id) {
    console.log('delete');
    const url = '/api/answer/delete'
    let params = {
      answer_id: answer_id
    }
    fastapi('delete', url, params,
      (json) => {
        window.confirm('삭제?')
        get_detail_info()
      },
      (json_error) => {error=json_error}
    )
  }
</script>




<div class="container">
  <h2 class="border-bottom py-3 mt-3">{question.subject}</h2>

  <Error error={error} />

  <div class="card mt-3">
    <div class="card-body">
      <div>{question.content}</div>
      <div class="d-flex justify-content-end">
        <div class="badge bg-light text-dark text-start">
          <div>{question.user.username}</div>
          <div>{question.create_date}</div>
        </div>
      </div>
      {#if $is_login}
      <button class="btn btn-secondary" on:click={questionVote(question.id)}>
        추천
        <span class="badge rounded-pill text-dark bg-light">{question.voter.length}</span>
      </button>
        {#if $username == question.user.username}
        <a use:link href="/question-modify/{question.id}" class="btn btn-secondary">수정</a>        
        <button class="btn btn-danger" on:click={questionDel(question.id)}>삭제</button>
        {/if}
      {/if}
    </div>
  </div>
  <a use:link href="/" class="btn btn-dark mt-3" >목록으로</a>

  
  <h3 class="border-bottom py-3 mt-3">
    {question.question_answers.length}개의 답변이 있습니다.
  </h3>
  {#each question.question_answers as answer}
  <div class="card mt-3">
    <div class="card-body">
      <div>{answer.content}</div>
      <div class="d-flex justify-content-end">
        <div class="badge bg-light text-dark text-start">
          <div>{answer.user.username}</div>
          <div >{answer.create_date}</div>
        </div>
      </div>
      {#if $is_login}
      <button class="btn btn-secondary" on:click={answerVote(answer.id)}>
        추천
        <span class="badge rounded-pill bg-light text-dark">{answer.voter.length}</span>
      </button>        
        {#if answer.user.username == $username}
        <a use:link href="/answer-modify/{answer.id}" class="btn btn-secondary">수정
        </a>
        <button class="btn btn-danger" on:click={answerDel(answer.id)}>삭제</button>
        {/if}
      {/if}
    </div>
  </div>
  {/each}

  <form class="mt-3" method="post">
    <textarea rows=15 class="form-control" bind:value={content} disabled={$is_login ? '': 'disabled'}></textarea>
  </form>
  <button class="btn btn-dark mt-3 {$is_login ? '': 'disabled'}" on:click={postAnswer}>답변저장</button>
  

</div>