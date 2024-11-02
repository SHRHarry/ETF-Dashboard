import React, { useContext } from "react";

const Header = ({ title }) => {
    return (
        // <div className="has-text-centered m-6">
        //     <h1 className="title">{title}</h1>
        // </div>
        <section class="hero is-small has-text-centered m-3">
            <div class="hero-body">
                <div class="container">
                    <h1 class="title">
                    {title}
                    </h1>
                </div>
            </div>
        </section>
      );
}

export default Header;