<script>
    export let error = '' // 프론트에서 전달받은 error
</script>

{#if error.detail.length > 0}
{#each error.detail as err}        
<div class="alert alert-danger" role="alert">
    <div style="font-weight:700;">{err['loc'][1]}: {err['msg']}</div>
</div>
{/each}
{/if}