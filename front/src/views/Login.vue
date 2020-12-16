<template>
<b-container>  
  <div style="margin-top: 10rem">
    <div>
      <b-tabs content-class="mt-3">
        <b-tab title="Entrar" active>
          <b-alert v-model="showError" variant="danger" dismissible>
            Usuario / contraseña incorrectos
          </b-alert>
          <b-form @submit="onSubmit">
            <b-form-group
              id="input-group-1"
              type="email"
              label="Email:"
              label-for="input-username"
            >
              <b-form-input
                id="input-username"
                v-model="form.username"
                type="text"
                placeholder="juancar@rey.es"
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
        </b-tab>
        <b-tab title="Registrarse">
        <b-alert v-model="showError" variant="danger" dismissible>
            Error en el registro
          </b-alert>
        <b-form @submit="onRegisterSubmit">
            <b-form-group
              id="input-group-1"
              label="Email:"
              label-for="input-username"
            >
              <b-form-input
                id="input-username"
                v-model="form.username"
                type="email"
                placeholder="juancar@rey.es"
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

            <b-form-group
              id="input-group-2"
              label="Nombre:"
              label-for="input-name"
            >
              <b-form-input
                id="input-name"
                v-model="form.name"
                placeholder="Juan Carlos"
                required
              ></b-form-input>
            </b-form-group>

            <b-form-group
              id="input-group-3"
              label="Apellidos:"
              label-for="input-surname"
            >
              <b-form-input
                id="input-surname"
                v-model="form.surname"
                placeholder="Borbón"
                required
              ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-4">
              <b-button variant="primary" type="submit">Registrarte</b-button>
            </b-form-group>
          </b-form>
        </b-tab>        
      </b-tabs>
    </div>
  </div>
  
</b-container>
</template>

<script>
  export default {
    data() {
      return {
        form: {
          username: '',
          email: '',
          password: '',
          name: '',
          surname: '',
        },
        showError: false
      }
    },
    methods: {
      async onSubmit(event) {
        event.preventDefault();
        this.$store.commit("SET_SHOWSPINNER", true);
        this.form.email = this.form.username;
        const response = await this.$store.dispatch("login", JSON.stringify(this.form));
        const token = response.access;
        this.$store.commit("SET_SHOWSPINNER", false);
        if (token === undefined){
          this.showError = true;          
        } else {
          this.$store.commit('SET_CURRENTUSER', {username: this.form.username, token: token});          
          this.$router.push("/home");
        }
      },
      async onRegisterSubmit(event) {
        event.preventDefault();
        this.form.email = this.form.username;
        const response = await this.$store.dispatch("register", JSON.stringify(this.form));
        const email = response.email;
        if (email === undefined){
          this.showError = true
        } else {
          this.onSubmit(event);
        }
      }
    }
  }
</script>
