

import streamlit as st
import pandas as pd
import plotly.express as px

from port_mapping import create_port_mapping, xor_bits
from simon_solver import run_simon
from simon_recovery import recover_secret, dot_product_mod2

st.set_page_config(
    page_title="Quantum Port Inspector",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM DESIGN ----------
st.markdown("""
<style>
/* Main page */
.stApp {
    background: linear-gradient(135deg, #07111f, #101d35);
    color: #f1f7ff;
}

[data-testid="stHeader"] {
    background: #07111f;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Headings */
h1, h2, h3 {
    color: #55e7ff !important;
}

p, label, li {
    color: #dce9f7;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #101e33;
}

[data-testid="stSidebar"] * {
    color: #eaf6ff;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #162b46;
    border: 1px solid #35bde5;
    border-radius: 14px;
    padding: 18px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #a9c9e8 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Dropdown and other input fields */
div[data-baseweb="select"] > div {
    background-color: #203650;
    border: 1px solid #35bde5;
}

div[data-baseweb="select"] span {
    color: #ffffff !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #00c9e8, #38bdf8);
    color: #07111f !important;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    min-height: 44px;
}

div.stButton > button:hover {
    background: #8af0ff;
    color: #07111f !important;
    border: 1px solid #ffffff;
}

/* Data tables: use a dark, readable theme */
[data-testid="stDataFrame"] {
    border: 1px solid #315577;
    border-radius: 10px;
}

/* Code / circuit panel */
[data-testid="stCode"] {
    background: #101e33 !important;
    border: 1px solid #315577;
    border-radius: 12px;
}

[data-testid="stCode"] pre,
[data-testid="stCode"] code {
    color: #dff7ff !important;
    background: transparent !important;
}

/* Expandable information */
[data-testid="stExpander"] {
    background: #142640;
    border: 1px solid #315577;
    border-radius: 10px;
}

/* Status messages */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* Dividers */
hr {
    border-color: #294562;
}
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.title("⚛️ Quantum Port Inspector")
st.caption(
    "SIMON'S ALGORITHM  |  PORT-MAPPING ANOMALY DETECTION"
)

st.markdown(
    "Detect a hidden XOR relationship using quantum measurements "
    "and classical post-processing."
)

# ---------- SIDEBAR CONTROLS ----------
with st.sidebar:
    st.header("🧪 Experiment Control")

    secret = st.selectbox(
        "Hidden oracle secret",
        ["001", "010", "011", "100", "101", "110", "111"],
        index=4
    )

    shots = st.slider(
        "Measurement shots",
        min_value=256,
        max_value=4096,
        value=1024,
        step=256
    )

    run = st.button(
        "▶ Run Analysis",
        width="stretch"
    )


# ---------- RUN EXPERIMENT ----------
if run:
    with st.spinner("Running quantum simulation..."):
        mapping = create_port_mapping(secret)
        circuit, counts = run_simon(secret, shots=shots)

        # Recovery receives measurement counts, not the secret.
        recovered = recover_secret(counts)

        st.session_state["analysis"] = {
            "selected_secret": secret,
            "mapping": mapping,
            "circuit": circuit,
            "counts": counts,
            "recovered": recovered,
            "shots": shots
        }


# ---------- SHOW INITIAL STATE ----------
if "analysis" not in st.session_state:
    st.info("Choose a hidden secret in the sidebar and click Run Analysis.")
    st.stop()

data = st.session_state["analysis"]

# Avoid presenting old results as though they came from new settings.
if (
    data["selected_secret"] != secret
    or data["shots"] != shots
):
    st.warning("Settings changed. Click Run Analysis to update the results.")
    st.stop()

mapping = data["mapping"]
circuit = data["circuit"]
counts = data["counts"]
recovered = data["recovered"]

# ---------- METRICS ----------
st.divider()

m1, m2, m3, m4 = st.columns(4)

m1.metric("Input Ports", "8")
m2.metric("Unique Outputs", "4")
m3.metric("Measurement Shots", data["shots"])
m4.metric("Recovered Secret", recovered)

# ---------- PORT MAPPING ----------
st.subheader("01 · Port Mapping Topology")

port_rows = []

for x in sorted(mapping):
    port_rows.append({
        "Input Port": x,
        "Output Port": mapping[x],
        "Paired Input": xor_bits(x, recovered)
    })

port_df = pd.DataFrame(port_rows)

st.dataframe(
    port_df,
    width="stretch",
    hide_index=True,
    height=310
)

# ---------- MEASUREMENT CHART ----------
st.subheader("02 · Quantum Measurement Results")

chart_df = pd.DataFrame([
    {"Measurement": y, "Frequency": count}
    for y, count in sorted(counts.items())
])

fig = px.bar(
    chart_df,
    x="Measurement",
    y="Frequency",
    text="Frequency",
    color="Frequency",
    color_continuous_scale=["#1684b5", "#49efff"],
    template="plotly_dark",
    title="Measured bitstring frequencies"
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#eaf6ff"),
    title_font_color="#55e7ff",
    xaxis_title="Measured bitstring",
    yaxis_title="Number of measurements",
    coloraxis_showscale=False,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(fig, width="stretch")



# ---------- DOWNLOADABLE EXPERIMENT REPORT ----------
st.subheader("08 · Export Experiment Report")

st.write(
    "Download the quantum measurement results and port mapping "
    "in an Excel-friendly CSV file."
)

# Measurement results
measurement_report = pd.DataFrame([
    {
        "Selected Secret": f'="{data["selected_secret"]}"',
        "Recovered Secret": f'="{recovered}"',
        "Measured Bitstring": f'="{y}"',
        "Frequency": frequency,
        "Orthogonality Value": dot_product_mod2(y, recovered),
        "Verification": (
            "PASS"
            if dot_product_mod2(y, recovered) == 0
            else "FAIL"
        ),
        "Total Shots": data["shots"]
    }
    for y, frequency in sorted(counts.items())
])

# Port mapping results
port_report = pd.DataFrame([
    {
        "Input Port": f'="{x}"',
        "Output Port": mapping[x],
        "Paired Input": f'="{xor_bits(x, recovered)}"'
    }
    for x in sorted(mapping)
])

# Add a section label between the two tables.
separator = pd.DataFrame([{
    "Selected Secret": "PORT MAPPING",
    "Recovered Secret": "",
    "Measured Bitstring": "",
    "Frequency": "",
    "Orthogonality Value": "",
    "Verification": "",
    "Total Shots": "",
    "Input Port": "",
    "Output Port": "",
    "Paired Input": ""
}])

report = pd.concat(
    [
        measurement_report,
        separator,
        port_report
    ],
    ignore_index=True
)

st.download_button(
    label="⬇ Download Experiment Report (CSV)",
    data=report.to_csv(index=False).encode("utf-8-sig"),
    file_name=f"simon_experiment_{recovered}.csv",
    mime="text/csv",
    width="stretch"
)


# ---------- QUANTUM CIRCUIT ----------
st.subheader("03 · Quantum Circuit")

st.caption(
    "Three input qubits, three output qubits, an oracle, "
    "Hadamard gates and input-register measurements."
)

st.code(
    circuit.draw(output="text"),
    language="text",
    wrap_lines=False
)

# ---------- ORTHOGONALITY CHECK ----------
st.subheader("04 · Orthogonality Verification")

verification_rows = []

for y, frequency in sorted(counts.items()):
    value = dot_product_mod2(y, recovered)

    verification_rows.append({
        "Measured y": y,
        "Count": frequency,
        "y · s mod 2": value,
        "Status": "PASS" if value == 0 else "FAIL"
    })

verification_df = pd.DataFrame(verification_rows)

st.dataframe(
    verification_df,
    width="stretch",
    hide_index=True
)

all_valid = all(
    row["y · s mod 2"] == 0
    for row in verification_rows
)

if recovered == secret and all_valid:
    st.success(
        f"Secret recovered correctly: {recovered}. "
        "All measured strings satisfy y · s = 0 (mod 2)."
    )
else:
    st.error(
        "Recovery or verification failed. "
        "Inspect the measurement equations before trusting the result."
    )

# ---------- CLASSICAL POST-PROCESSING ----------
with st.expander("📘 Classical Post-Processing Explained"):
    st.markdown("""
    Each measured bitstring **y** gives a binary linear equation:

    **y · s = 0 (mod 2)**

    The classical recovery routine tests the seven possible
    nonzero 3-bit secrets and finds the candidate consistent
    with the measured equations.

    If multiple candidates remain, additional independent
    measurements are needed. Repeating the same equation
    does not provide additional independent information.
    """)

# ---------- RECOVERY EXPLAINER ----------
st.subheader("05 · Step-by-Step Classical Recovery")

st.write(
    "Each measurement y gives an equation y · s = 0 (mod 2). "
    "The classical solver checks which nonzero secrets satisfy "
    "all the measured equations."
)

from itertools import product

candidate_secrets = [
    "".join(bits)
    for bits in product("01", repeat=3)
    if "".join(bits) != "000"
]

recovery_rows = []

for candidate in candidate_secrets:
    equation_results = [
        dot_product_mod2(y, candidate) == 0
        for y, count in counts.items()
        if count > 0
    ]

    recovery_rows.append({
        "Candidate secret": candidate,
        "Equations satisfied": sum(equation_results),
        "Total equations": len(equation_results),
        "Status": (
            "CONSISTENT"
            if all(equation_results)
            else "ELIMINATED"
        )
    })

recovery_df = pd.DataFrame(recovery_rows)

st.dataframe(
    recovery_df,
    width="stretch",
    hide_index=True
)

remaining = recovery_df[
    recovery_df["Status"] == "CONSISTENT"
]["Candidate secret"].tolist()

if len(remaining) == 1:
    st.success(
        f"Only one candidate remains: {remaining[0]}. "
        "The measurement equations uniquely identify the secret."
    )
elif len(remaining) > 1:
    st.warning(
        f"{len(remaining)} candidates remain: {remaining}. "
        "More independent measurement equations are needed."
    )
else:
    st.error(
        "No candidate satisfies every equation. "
        "Check the circuit and measurement results."
    )

# ---------- FINAL REPORT ----------
st.subheader("06 · Anomaly Detection Report")

r1, r2 = st.columns(2)

with r1:
    st.markdown("**Recovered XOR relationship**")
    st.code(f"s = {recovered}")

    st.markdown("**Input-to-partner rule**")
    st.code(f"partner(x) = x XOR {recovered}")

with r2:
    st.markdown("**Verification status**")
    if recovered == secret and all_valid:
        st.success("SIMULATION PASSED")
        st.write("Eight inputs form four two-member output groups.")
    else:
        st.error("CHECK REQUIRED")
        st.write("The selected oracle and recovered result need investigation.")

st.caption(
    "Educational quantum simulation only. "
    "No physical network switch is connected."
)


# ---------- QUANTUM VS CLASSICAL COMPARISON ----------
st.subheader("07 · Quantum vs Classical Analysis")

st.markdown(
    "Both approaches can identify the hidden relationship in this "
    "small simulator. They use different information to do it."
)

comparison_df = pd.DataFrame([
    {
        "Feature": "Input information",
        "Quantum approach": "Measurement results from Simon's circuit",
        "Classical approach": "Direct access to the complete port mapping"
    },
    {
        "Feature": "Main technique",
        "Quantum approach": "Superposition, oracle queries and interference",
        "Classical approach": "Compare input-output pairs"
    },
    {
        "Feature": "Secret recovery",
        "Quantum approach": "Binary equations from measured bitstrings",
        "Classical approach": "XOR inputs that share an output"
    },
    {
        "Feature": "For this 3-bit example",
        "Quantum approach": "Requires repeated measurements and post-processing",
        "Classical approach": "Simple and computationally inexpensive"
    },
    {
        "Feature": "Scaling insight",
        "Quantum approach": "Simon has an exponential oracle-query advantage under its promise",
        "Classical approach": "Generic black-box approaches may require many more queries"
    }
])

st.dataframe(
    comparison_df,
    width="stretch",
    hide_index=True
)

st.info(
    "This is an educational simulator, not a benchmark proving that "
    "a quantum computer runs faster than a classical computer. "
    "The classical comparison assumes direct access to the mapping, "
    "while Simon's algorithm treats the mapping as a black-box oracle."
)
