import React from "react";
import Table from "../components/UI/table/table";

const About = () => {
    const httpUrl = 'http://localhost:8000/costumers';

    return (
        <div>


            <Table FetchUrl={httpUrl}></Table>
        </div>
    );
};
export default About;