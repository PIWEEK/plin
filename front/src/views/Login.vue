<template>
<b-container>  
  <div style="margin-top: 10rem">
    <b-alert v-model="showError" variant="danger" dismissible>
      Usuario / contraseña incorrectos
    </b-alert>
    <b-form @submit="onSubmit">
      <b-form-group
        id="input-group-1"
        label="Nombre de usuario:"
        label-for="input-username"
      >
        <b-form-input
          id="input-username"
          v-model="form.username"
          type="text"
          placeholder="morpheo"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Password:" label-for="input-password">
        <b-form-input
          type="password"
          id="input-password"
          v-model="form.password"
          placeholder="password"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group id="input-group-3">
        <b-button variant="primary" type="submit">Entrar</b-button>
      </b-form-group>
    </b-form>
  </div>
  
</b-container>
</template>

<script>
  export default {
    data() {
      return {
        form: {
          username: '',
          password: '',          
        },
        showError: false
      }
    },
    methods: {
      async onSubmit(event) {
        event.preventDefault();
        const response = await this.$store.dispatch("login", JSON.stringify(this.form));
        const token = response.access;
        if (token === undefined){
          this.showError = true
        } else {
          this.$store.commit('SET_CURRENTUSER', {username: this.form.username, token: token});
          this.$router.push("/home");
        }
      }
    }
  }
</script>
