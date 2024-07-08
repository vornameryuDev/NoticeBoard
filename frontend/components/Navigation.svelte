<script>
  import {link} from 'svelte-spa-router';
  import {access_token, username, is_login, keyword} from '../src/lib/store';



  function logout() {
    $access_token = '';
    $username = '';
    $is_login = false;
  }
</script>

<nav class="navigation bg-light">
    <div class="nav-box">

      <div class="logo-icon">
        <a use:link href="/" on:click={() => {$keyword=''}}>Notice</a>
      </div>

      <div class="nav-icon-box">
        {#if $is_login }
        <span class="nav-button">
          <a use:link href="/user-login" on:click={logout} >로그아웃({$username})</a>
        </span>
        {:else}
        <span class="nav-button">
          <a use:link href="/user-create">회원가입</a>
        </span>
        <span class="nav-button">
          <a use:link href="/user-login">로그인</a>
        </span>
        {/if}
      </div>

    </div>
</nav>