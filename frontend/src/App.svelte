<script>  
  /*
  svelte-spa-router사용
  */

  import Router from "svelte-spa-router";
  import Navigation from "../components/Navigation.svelte";
  import Home from "../routes/Home.svelte";
  import Detail from "../routes/Detail.svelte";
  import UserCreate from "../routes/UserCreate.svelte";
  import UserLogin from "../routes/UserLogin.svelte";
  import QuestionCreate from "../routes/QuestionCreate.svelte";
  import QuestionModify from "../routes/QuestionModify.svelte";
  import AnswerModify from "../routes/AnswerModify.svelte";

  const routes = {
    '/': Home,
    '/detail/:question_id': Detail,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/question-create': QuestionCreate,
    '/question-modify/:question_id': QuestionModify,
    '/answer-modify/:answer_id': AnswerModify,
  }
</script>

<Navigation />

<Router {routes}/>

