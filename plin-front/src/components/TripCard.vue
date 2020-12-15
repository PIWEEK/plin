<template>
<div>
  <b-card
    :img-src="image"
    img-alt="Image"
    img-top
    tag="article"
    style="max-width: 20rem; margin: 1rem"
    class="mb-2"
  >
    <b-card-text>
      {{ name }}
    </b-card-text>

    <b-button href="#" variant="primary" v-on:click="selectTrip">Go!</b-button>
  </b-card>
</div>
</template>

<script>
    export default {
      props: ["id", "name", "image"],      
      methods: {
        selectTrip: function () {
          this.$store.commit('SET_CURRENTTRIP', {id:this.id, name: this.name, image: this.image});
          this.$router.push("/trip")          
        }
      }
      
    }
</script>

<style lang="scss" scoped>

</style>