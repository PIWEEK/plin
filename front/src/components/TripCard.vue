<template>
<div>
  <b-card
    :img-src="image"
    img-alt="Image"
    img-top
    tag="article"
    style="width: 15rem; height:20rem; margin: 1rem; cursor: pointer"
    class="mb-2"
    v-on:click="selectTrip"
  >
    <b-card-text>
      <h4 style="height: 4rem">
        {{ name }}
      </h4>
      <div>
        <span v-if="start !== null">Del {{ start }} </span>
        <span v-if="end !== null">al {{ end }} </span>
        ({{ duration }} días)
      </div>
    </b-card-text>
  </b-card>
</div>
</template>

<script>
    export default {
      props: ["id", "name", "image", "start", "end", "duration"],      
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