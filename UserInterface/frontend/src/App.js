import React, { Component } from "react";
import Modal from "./components/Modal";
import Test from "./components/Test";
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      wafs: [],
      modal: false,
      testing: false,
      activeItem: {
        id: "",
        name: "",
        description: "",
        waf_address: "",
        app_address: "",
        total_requests: 0,
        average_time: 0.0,
        allowed_requests: 0,
        blocked_requests: 0,
        threats_detected: 0,
        app_enabled: false,
        waf_enabled: false,
        settings: {
          block_remote_addr: false,
          block_user_agent: false,
          block_path: false,
          block_query_string: false,
          check_token: false,
          check_signature: false,
          check_anomaly: false
        },
        rules: {
          blocked_ips: [],
          blocked_user_agents: [],
          blocked_paths: [],
          blocked_query_strings: []
        },
        results: {
          balanced: {
            tpr: 0.0,
            tnr: 0.0
          },
          conventional: {
            tpr: 0.0,
            tnr: 0.0
          },
          unconventional: {
            tpr: 0.0,
            tnr: 0.0
          }
        }
      }
    };
  }

  componentDidMount() {
    this.refreshList();
    document.title = 'WAF Overview';
  }

  refreshList = () => {
    axios
      .get("/api/wafs/")
      .then((res) => this.setState({ wafs: res.data }))
      .catch((err) => console.log(err));
  };

  toggle_modal = () => {
    this.setState({ modal: !this.state.modal });
  };

  toggle_testing = () => {
    this.setState({ testing: !this.state.testing });
  };

  handleSubmit = (item) => {
    this.toggle_modal();
    this.handleUpdate(item);
  };

  handleTesting = (item) => {
    this.toggle_testing();
    this.handleUpdate(item);
  };

  handleUpdate = (item) => {
    if (item.id) {
      axios
        .put(`/api/wafs/${item.id}/`, item)
        .then((res) => this.refreshList());
      return;
    }
    axios
      .post("/api/wafs/", item)
      .then((res) => this.refreshList());
  };

  handleDelete = (item) => {
    axios
      .delete(`/api/wafs/${item.id}/`)
      .then((res) => this.refreshList());
  };

  createItem = () => {
    const item = {
      id: "",
      name: "",
      description: "",
      waf_address: "",
      app_address: "",
      total_requests: 0,
      average_time: 0.0,
      allowed_requests: 0,
      blocked_requests: 0,
      threats_detected: 0,
      app_enabled: false,
      waf_enabled: false,
      settings: {
        block_remote_addr: false,
        block_user_agent: false,
        block_path: false,
        block_query_string: false,
        check_token: false,
        check_signature: false,
        check_anomaly: false
      },
      rules: {
        blocked_ips: [],
        blocked_user_agents: [],
        blocked_paths: [],
        blocked_query_strings: []
      },
      results: {
        balanced: {
          tpr: 0.0,
          tnr: 0.0
        },
        conventional: {
          tpr: 0.0,
          tnr: 0.0
        },
        unconventional: {
          tpr: 0.0,
          tnr: 0.0
        }
      }
    };

    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  editItem = (item) => {
    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  testItem = (item) => {
    this.setState({ activeItem: item, testing: !this.state.testing });
  };

  startApp = async (app) => {
    const response = await axios.post(`/api/wafs/start_app/`, app);
    this.refreshList();
    return response.data;
  };

  stopApp = async (app) => {
    const response = await axios.post(`/api/wafs/stop_app/`, app);
    this.refreshList();
    return response.data;
  };

  startWAF = async (app) => {
    const response = await axios.post(`/api/wafs/start_waf/`, app);
    this.refreshList();
    return response.data;
  };

  stopWAF = async (app) => {
    const response = await axios.post(`/api/wafs/stop_waf/`, app);
    this.refreshList();
    return response.data;
  };

  render() {
    const { wafs, modal, testing, activeItem } = this.state;
    console.log(wafs);

    return (
      <div className="container">
      <header>
        <h1>Web Application Firewall Overview</h1>
      </header>
      <main>
        <div className="row">
        {wafs.map((app, index) => (
          <div className="col-md-4" key={index}>
            <div className="card">
              <div className="card-body">
              <h2 className="card-title">{app.name}</h2>
              <h5>WAF Information</h5>
              <p className="card-text">Description: {app.description}</p>
              <p className="card-text">WAF Address: {app.waf_address}</p>
              <p className="card-text">App Address: {app.app_address}</p>
              <p className="card-text">Total Requests: {app.total_requests}</p>
              <p className="card-text">Average Time: {app.average_time}%</p>
              <p className="card-text">Allowed Requests: {app.allowed_requests}</p>
              <p className="card-text">Blocked Requests: {app.blocked_requests}</p>
              <p className="card-text">App Enabled: {app.app_enabled ? "Yes" : "No"}</p>
              <p className="card-text">WAF Enabled: {app.waf_enabled ? "Yes" : "No"}</p>     
              <h5>Configure</h5>
              <div className="button-container">
                <button
                className="btn btn-danger"
                onClick={() => {
                  if (window.confirm("Are you sure you want to delete this item?")) {
                    this.handleDelete(app);
                  }
                }}
                >
                Delete
                </button>
                <button
                className="btn btn-primary"
                onClick={this.createItem}
                >
                Add
                </button>
                <button
                className="btn btn-primary"
                onClick={() => this.editItem(app)}
                >
                View/Edit
                </button>
                <button
                className="btn btn-primary"
                onClick={() => this.testItem(app)}
                >
                Test
                </button>
              </div>
              <h5>WAF Actions</h5>
              <div className="button-container">
                <button
                className="btn btn-primary"
                onClick={async () => {
                  const data = await this.startWAF(app);
                  alert(data.status);
                }}
                >
                Start WAF
                </button>
                <a href={"http://" + app.waf_address + ":500" + app.id + "/"} target="_blank" rel="noopener noreferrer">
                  <button
                  className="btn btn-primary"
                  >
                  View WAF
                  </button>
                </a>
                <button
                className="btn btn-primary"
                onClick={async () => {
                  const data = await this.stopWAF(app);
                  alert(data.status);
                }}
                >
                Stop WAF
                </button>
              </div>
              <h5>App Actions</h5>
              <div className="button-container">
                <button
                className="btn btn-primary"
                onClick={async () => {
                  const data = await this.startApp(app);
                  alert(data.status);
                }} 
                >
                Start App
                </button>
                <a href={"http://" + app.app_address + ":800" + app.id + "/"} target="_blank" rel="noopener noreferrer">
                  <button
                  className="btn btn-primary"
                  >
                  View App
                  </button>
                </a>
                <button
                className="btn btn-primary"
                onClick={async () => {
                  const data = await this.stopApp(app);
                  alert(data.status);
                }}
                >
                Stop App
                </button>
              </div>
            </div>
          </div>
          </div>
        ))}
        </div>
      </main>
      <footer>
        <p>WebAppFirewall - EPR402 2024</p>
      </footer>
      {modal ? (
        <Modal
        activeItem={activeItem}
        toggle={this.toggle_modal}
        onSave={this.handleSubmit}
        />
      ) : null}
      {testing ? (
        <Test
        activeItem={activeItem}
        toggle={this.toggle_testing}
        onSave={this.handleTesting}
        />
      ) : null}
      </div>
    );
  }
}

export default App;
