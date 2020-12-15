<template>
  <b-card
    :img-src="image"
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 10rem;"
    class="mb-6"
  >
    <b-card-text>
      {{ name }}
    </b-card-text>
  </b-card>
</template>

<script>    
    export default {
      props: ["id", "name", "image"],
    }
</script>

<style lang="scss" scoped>
</style>