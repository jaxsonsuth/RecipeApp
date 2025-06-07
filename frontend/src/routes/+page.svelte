<script>
  let recipe = null;
  let loading = false;
  let error = null;

  async function fetchRecipe() {
    loading = true;
    error = null;
    try {
      const res = await fetch('http://backend:8000/random_recipe');
      if (!res.ok) throw new Error('Failed to fetch recipe');
      recipe = await res.json();
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }
</script>

<button on:click={fetchRecipe}>
  {loading ? 'Loading...' : 'Get Random Recipe'}
</button>

{#if error}
  <p style="color: red;">Error: {error}</p>
{:else if recipe}
  <div style="margin-top: 1rem;">
    <h2>{recipe.title}</h2>
    <h3>Ingredients</h3>
    <ul>
      {#each recipe.ingredients as ingredient}
        <li>{ingredient}</li>
      {/each}
    </ul>
    <h3>Instructions</h3>
    <p>{recipe.instructions}</p>
  </div>
{/if}
