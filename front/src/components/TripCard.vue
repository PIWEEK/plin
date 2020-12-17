<template>
<div>
  <b-card
    tag="article"
    style="width: 15rem; height:20rem; margin: 1rem; cursor: pointer"
    class="mb-2"
    v-on:click="selectTrip"
  >
    <b-card-img :src="url_picture" alt="Image" center style="object-fit: scale-down;"></b-card-img>

    <b-card-text>
      <h4 style="height: 4rem">
        {{ title }}
      </h4>
      <div>
        <span v-if="start">Del {{ start }} </span>
        <span v-if="end">al {{ end }} </span>
        ({{ duration }} días)
      </div>
    </b-card-text>
  </b-card>
</div>
</template>

<script>
    export default {
      props: ["id", "title", "url_picture", "start", "end", "duration"],      
      methods: {
        selectTrip: function () {
          this.$store.commit('SET_CURRENTTRIP', {id:this.id, title: this.title, url_picture: this.url_picture});
          this.$router.push("/trip");
        }
      }
    }
</script>

<style lang="scss" scoped>

</style>