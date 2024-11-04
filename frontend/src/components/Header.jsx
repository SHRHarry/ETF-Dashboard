import React, { useContext } from "react";

const Header = ({ title }) => {
    return (
        <section class="hero is-small has-text-centered" style={{ background: "linear-gradient(135deg, #8e2de2, #4a00e0)"}}>
            <div class="hero-body">
                <div class="container">
                    <h1 class="title has-text-white">
                    {title}
                    </h1>
                </div>
            </div>
        </section>
      );
}

export default Header;