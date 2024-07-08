<script>
  import {link} from 'svelte-spa-router';
  import fastapi from '../src/lib/api';
  import {is_login, keyword} from '../src/lib/store';

  let question_list = [];
  let kw = '';


  function get_question_list(){
    const url = '/api/question/list';
    let params = {
      kw: $keyword
    }
    fastapi('get', url, params,
      (json) => {question_list = json, kw=$keyword}
    )
  }

  $: $keyword, get_question_list(); // keyword값이 변경되면 get_question_list를 실행
</script>

<div class="container mt-3">

  <div class="d-flex justify-content-end">
    <div class="col-6 my-3">
      <div class="input-group">
          <input type="text" class="form-control" bind:value={kw}>
          <button class="btn btn-outline-secondary" on:click={() => {$keyword=kw}}>
              찾기
          </button>
      </div>
    </div>
  </div>

  <table class="table">
    <thead class="table-dark">
      <tr>
        <td>번호</td>
        <td>제목</td>
        <td>글쓴이</td>
        <td>작성날짜</td>
      </tr>
    </thead>
    <tbody>
      {#each question_list as question}
      <tr>
        <td>{question.id}</td>
        <td>
          <a use:link href="/detail/{question.id}">{question.subject}</a>
        </td>
        <td>{question.user.username}</td>
        <td>{question.user.create_date}</td>
      </tr>
      {/each}      
    </tbody>
  </table>

  {#if $is_login}
  <a use:link href="/question-create" class="btn btn-dark">질문등록</a>    
  {/if}
</div>

