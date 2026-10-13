import streamlit as st
from pathlib import Path

# ============================================================
# RENOVA MODERN UI
# Presentation layer only
# ============================================================
def _load_renova_ui():
    css_file = Path(__file__).parent / "assets" / "renova_ui.css"

    if css_file.exists():
        st.markdown(
            f"<style>{css_file.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )

from pathlib import Path
import zipfile
import re


# ============================================================
# EXISTING PROJECT MODULES
# ============================================================

from src.reuse_analyzer import analyze_project
from src.database import (
    initialize_database,
    create_user,
    authenticate_user,
    add_project,
    get_user_projects,
)


# ============================================================
# INITIALIZE
# ============================================================

initialize_database()

BASE = Path(__file__).resolve().parent

DATA = BASE / "data" / "components.csv"

UPLOAD_ROOT = BASE / "uploads"

UPLOAD_ROOT.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# PAGE
# ============================================================

_load_renova_ui()

st.set_page_config(
    page_title="RENOVA",
    page_icon="♻️",
    layout="wide",
)


# ============================================================
# SESSION
# ============================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "ai_queries" not in st.session_state:
    st.session_state.ai_queries = 0

if "reuse_matches" not in st.session_state:
    st.session_state.reuse_matches = 0


# ============================================================
# TECH THEME
# ============================================================

st.markdown(
r"""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 5% 10%,
            rgba(0, 220, 255, 0.10),
            transparent 25%
        ),
        radial-gradient(
            circle at 95% 95%,
            rgba(95, 68, 255, 0.13),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #020d1c 0%,
            #04223a 45%,
            #061f37 72%,
            #121843 100%
        ) !important;

    color: #f5f9fd !important;
}


/* Streamlit */

header[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

footer {
    display: none !important;
}


/* Sidebar */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #020d1b,
            #041a2e
        ) !important;

    border-right:
        1px solid
        rgba(36, 209, 255, 0.20) !important;
}

[data-testid="stSidebar"] * {
    color: #edf7fc !important;
}

[data-testid="stSidebar"] button {
    border-radius: 10px !important;

    min-height: 44px !important;

    margin-bottom: 5px !important;

    background:
        rgba(8, 42, 68, 0.72) !important;

    border:
        1px solid
        rgba(57, 191, 240, 0.18) !important;

    color:
        #edf7fc !important;
}

[data-testid="stSidebar"] button:hover {
    background:
        rgba(10, 103, 141, 0.45) !important;

    border-color:
        #23dfff !important;
}


/* Main title */

h1, h2, h3 {
    color: #f5f9fd !important;
}

h1 {
    font-weight: 800 !important;
}


/* Metrics */

[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            rgba(7, 43, 71, 0.95),
            rgba(3, 24, 42, 0.95)
        );

    border:
        1px solid
        rgba(32, 207, 255, 0.25);

    border-radius:
        15px;

    padding:
        16px;
}

[data-testid="stMetricLabel"] {
    color: #8ea8ba !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-weight: 800 !important;
}


/* Cards */

.renova-card {
    background:
        linear-gradient(
            145deg,
            rgba(5, 39, 64, 0.95),
            rgba(3, 25, 45, 0.95)
        );

    border:
        1px solid
        rgba(37, 210, 255, 0.28);

    border-radius:
        17px;

    padding:
        20px;

    margin-top:
        16px;
}


/* AI card */

.ai-card {
    background:
        linear-gradient(
            135deg,
            rgba(4, 44, 72, 0.97),
            rgba(3, 25, 45, 0.97)
        );

    border:
        1px solid
        rgba(31, 216, 255, 0.43);

    border-radius:
        18px;

    padding:
        23px;
}


/* Text */

.muted {
    color: #91a8ba;
}


/* Inputs */

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background:
        #071d30 !important;

    color:
        #f2faff !important;

    border:
        1px solid
        rgba(111, 211, 238, 0.50) !important;

    border-radius:
        9px !important;
}

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color:
        #79a0b5 !important;

    opacity:
        1 !important;
}


/* Buttons */

div.stButton > button {
    border-radius:
        9px !important;

    min-height:
        42px !important;

    font-weight:
        650 !important;
}

.primary-renova button {
    background:
        linear-gradient(
            90deg,
            #10bfdc,
            #19e7aa
        ) !important;

    color:
        #03212d !important;

    border:
        1px solid
        #29efb0 !important;
}


/* Project cards */

.project-box {
    background:
        linear-gradient(
            145deg,
            rgba(7, 48, 78, 0.92),
            rgba(4, 29, 49, 0.92)
        );

    border:
        1px solid
        rgba(58, 203, 255, 0.23);

    border-radius:
        13px;

    padding:
        15px;

    min-height:
        110px;
}


/* Login */

.login-space {
    max-width:
        480px;

    margin:
        90px auto
        0 auto;
}

.login-card {
    background:
        linear-gradient(
            145deg,
            rgba(3, 21, 40, 0.97),
            rgba(5, 39, 58, 0.94)
        );

    border:
        1px solid
        rgba(36, 221, 255, 0.50);

    border-radius:
        22px;

    padding:
        35px;

    box-shadow:
        0 25px 65px
        rgba(0,0,0,0.35);
}

.login-brand {
    text-align:
        center;

    font-size:
        46px;

    font-weight:
        800;

    color:
        white;
}

.login-brand span {
    color:
        #25ddff;
}

.login-heading {
    text-align:
        center;

    font-size:
        32px;

    font-weight:
        750;

    color:
        white;

    margin-top:
        25px;
}

.login-subtitle {
    text-align:
        center;

    color:
        #91a8ba;

    font-size:
        13px;

    margin-bottom:
        25px;
}


/* Responsive */

@media (max-width: 800px) {

    .block-container {
        padding:
            10px !important;
    }

    .login-space {
        margin-top:
            30px;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HELPERS
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".js",
    ".ts",
    ".cpp",
    ".c",
    ".h",
    ".cs",
    ".html",
    ".css",
    ".sql",
    ".md",
    ".txt",
    ".json",
}


def safe_name(value):

    return re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        value.strip()
    )


def get_file_count(folder):

    folder = Path(folder)

    if not folder.exists():
        return 0

    ignored = {
        ".git",
        "__pycache__",
        "venv",
        ".venv",
        "node_modules",
    }

    count = 0

    for path in folder.rglob("*"):

        if not path.is_file():
            continue

        if any(
            item in ignored
            for item in path.parts
        ):
            continue

        if path.suffix.lower() in SUPPORTED_EXTENSIONS:

            count += 1

    return count


def get_language(folder):

    folder = Path(folder)

    mapping = {
        ".py": "Python",
        ".java": "Java",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".cpp": "C++",
        ".c": "C",
        ".cs": "C#",
    }

    counts = {}

    if not folder.exists():
        return "Project"

    for path in folder.rglob("*"):

        if not path.is_file():
            continue

        if path.suffix.lower() in mapping:

            ext = path.suffix.lower()

            counts[ext] = (
                counts.get(ext, 0) + 1
            )

    if not counts:
        return "Project"

    ext = max(
        counts,
        key=counts.get
    )

    return mapping[ext]


def go(page):

    st.session_state.page = page

    st.rerun()


# ============================================================
# AI SEARCH LOADERS
# ============================================================

@st.cache_resource(show_spinner=False)
def load_public_searcher():

    from src.semantic_search import SemanticSearcher

    return SemanticSearcher(DATA)


@st.cache_resource(show_spinner=False)
def load_private_searcher(folder):

    from src.project_search import ProjectSearcher

    return ProjectSearcher(
        Path(folder)
    )


# ============================================================
# LOGIN
# ============================================================

def login_page():

    left, center, right = st.columns(
        [1, 1.2, 1]
    )

    with center:

        st.markdown(
            '<div class="login-space">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-brand">'
            'REN<span>OVA</span>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.session_state.auth_mode == "login":

            st.markdown(
                '<div class="login-heading">Log in</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="login-subtitle">'
                'Sign in to your RENOVA account'
                '</div>',
                unsafe_allow_html=True
            )

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )

            if st.button(
                "Login →",
                type="primary",
                use_container_width=True
            ):

                user = authenticate_user(
                    username,
                    password
                )

                if user:

                    st.session_state.user = user
                    st.session_state.page = "Dashboard"
                    st.session_state.messages = []

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

            st.write("")

            if st.button(
                "Register",
                use_container_width=True
            ):

                st.session_state.auth_mode = "signup"

                st.rerun()

        else:

            st.markdown(
                '<div class="login-heading">'
                'Create Account'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="login-subtitle">'
                'Create your RENOVA account'
                '</div>',
                unsafe_allow_html=True
            )

            username = st.text_input(
                "Username",
                placeholder="Choose username",
                key="signup_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create password",
                key="signup_password"
            )

            confirm = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm password",
                key="signup_confirm"
            )

            if st.button(
                "Create Account",
                type="primary",
                use_container_width=True
            ):

                if password != confirm:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    success, message = create_user(
                        username,
                        password
                    )

                    if success:

                        st.success(
                            "Account created successfully."
                        )

                        st.session_state.auth_mode = "login"

                        st.rerun()

                    else:

                        st.error(
                            message
                        )

            if st.button(
                "Back to Login",
                use_container_width=True
            ):

                st.session_state.auth_mode = "login"

                st.rerun()

        st.markdown(
            '</div></div>',
            unsafe_allow_html=True
        )


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():

    username = st.session_state.user["username"]

    st.markdown(
        "## ♻️ RENOVA"
    )

    st.caption(
        "AI Software Intelligence"
    )

    st.write("")

    st.info(
        f"👤 {username}"
    )

    st.write("")

    if st.button(
        "🏠  Dashboard",
        use_container_width=True
    ):

        go("Dashboard")


    if st.button(
        "🤖  AI Assistant",
        use_container_width=True
    ):

        go("AI Assistant")


    if st.button(
        "📁  My Projects",
        use_container_width=True
    ):

        go("My Projects")


    if st.button(
        "⬆️  Upload Project",
        use_container_width=True
    ):

        go("Upload Project")


    if st.button(
        "🔎  Search Components",
        use_container_width=True
    ):

        go("AI Assistant")


    if st.button(
        "📜  History",
        use_container_width=True
    ):

        go("AI Assistant")


    if st.button(
        "👤  Profile",
        use_container_width=True
    ):

        st.info(
            f"Logged in as {username}"
        )


    st.divider()


    if st.button(
        "🚪  Logout",
        use_container_width=True
    ):

        st.session_state.user = None
        st.session_state.page = "Dashboard"
        st.session_state.messages = []

        st.rerun()


# ============================================================
# TOP BAR
# ============================================================

def top_bar():

    username = st.session_state.user["username"]

    a, b, c = st.columns(
        [3, 1, 1]
    )

    with a:

        st.markdown(
            "## ♻️ RENOVA"
        )

    with b:

        st.markdown(
            "🔔"
        )

    with c:

        st.markdown(
            f"👤 **{username}**"
        )

    st.divider()


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    top_bar()

    username = st.session_state.user["username"]

    projects = get_user_projects(
        st.session_state.user["id"]
    )

    project_count = len(projects)

    indexed_files = sum(
        get_file_count(
            project[3]
        )
        for project in projects
    )


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        f"# Welcome back, :blue[{username}] 👋"
    )

    st.caption(
        "Your AI-powered software reuse workspace"
    )


    # --------------------------------------------------------
    # STATS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "📁 My Projects",
            project_count
        )

    with c2:

        st.metric(
            "◈ Indexed Components",
            indexed_files
        )

    with c3:

        st.metric(
            "💬 AI Queries",
            st.session_state.ai_queries
        )

    with c4:

        st.metric(
            "♻️ Reuse Matches",
            st.session_state.reuse_matches
        )


    # --------------------------------------------------------
    # AI ASSISTANT
    # --------------------------------------------------------

    st.markdown(
        '<div class="ai-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "## 🤖 RENOVA AI Assistant"
    )

    st.write(
        "Ask about your project, reusable code, "
        "or previous projects."
    )

    st.caption(
        "RENOVA analyzes your requirement and finds "
        "relevant reusable components."
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    st.write(
        "**Try asking:**"
    )

    q1, q2, q3 = st.columns(3)

    with q1:

        if st.button(
            "💡 Face recognition attendance",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "I need a face recognition attendance system."
            )

            go("AI Assistant")


    with q2:

        if st.button(
            "🔐 Reusable authentication",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Find reusable authentication and login modules."
            )

            go("AI Assistant")


    with q3:

        if st.button(
            "🗄 Database integration",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Find reusable database integration components."
            )

            go("AI Assistant")


    prompt = st.text_area(
        "Requirement",
        placeholder="Describe the component or functionality...",
        height=85,
        label_visibility="collapsed",
        key="dashboard_requirement"
    )


    if st.button(
        "➤ Ask RENOVA",
        type="primary",
        use_container_width=True
    ):

        if prompt.strip():

            st.session_state.pending_prompt = (
                prompt.strip()
            )

            go("AI Assistant")

        else:

            st.warning(
                "Describe the functionality you need."
            )


    # --------------------------------------------------------
    # RECENT PROJECTS
    # --------------------------------------------------------

    st.markdown(
        "## 🕘 Recent Projects"
    )

    if not projects:

        st.info(
            "No projects uploaded yet. "
            "Upload your previous projects to build "
            "your private reuse knowledge base."
        )

        if st.button(
            "⬆️ Upload Project",
            use_container_width=True
        ):

            go("Upload Project")

    else:

        recent = projects[:3]

        cols = st.columns(
            len(recent)
        )

        for col, project in zip(
            cols,
            recent
        ):

            project_name = project[1]
            project_path = project[3]

            with col:

                st.markdown(
                    '<div class="project-box">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"### 📦 {project_name}"
                )

                st.caption(
                    get_language(project_path)
                )

                st.write(
                    f"◈ {get_file_count(project_path)} indexed files"
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


# ============================================================
# PUBLIC SEARCH
# ============================================================

def search_public(query):

    searcher = load_public_searcher()

    return searcher.search(
        query,
        5
    )


# ============================================================
# PRIVATE SEARCH
# ============================================================

def search_private(query):

    projects = get_user_projects(
        st.session_state.user["id"]
    )

    results = []

    for project in projects:

        project_path = project[3]
        project_name = project[1]
        project_id = project[0]

        try:

            searcher = load_private_searcher(
                project_path
            )

            matches = searcher.search(
                query,
                5
            )

            for match in matches:

                match["project_name"] = project_name
                match["project_id"] = project_id

                results.append(
                    match
                )

        except Exception as error:

            print(
                f"Project search error: {error}"
            )

    results.sort(
        key=lambda item:
            item.get(
                "score",
                0
            ),
        reverse=True
    )

    return results[:5]


# ============================================================
# AI ASSISTANT
# ============================================================

def ai_assistant():

    top_bar()

    st.markdown(
        "# 🤖 RENOVA AI Assistant"
    )

    st.caption(
        "Describe the component or functionality you need."
    )


    # --------------------------------------------------------
    # PENDING PROMPT
    # --------------------------------------------------------

    if st.session_state.pending_prompt:

        query = st.session_state.pending_prompt

        st.session_state.pending_prompt = None

        process_query(query)

    else:

        query = st.chat_input(
            "Describe the component or functionality..."
        )

        if query:

            process_query(
                query
            )


    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            if message["role"] == "assistant":

                public = message.get(
                    "public",
                    []
                )

                private = message.get(
                    "private",
                    []
                )

                if public:

                    st.markdown(
                        "### 🌐 Open-Source Matches"
                    )

                    for index, result in enumerate(
                        public,
                        1
                    ):

                        show_result(
                            result,
                            index,
                            "public"
                        )

                if private:

                    st.markdown(
                        "### 🔒 Your Project Matches"
                    )

                    for index, result in enumerate(
                        private,
                        1
                    ):

                        show_result(
                            result,
                            index,
                            "private"
                        )


# ============================================================
# QUERY
# ============================================================


def show_reuse_report(report):

    project_name = Path(
        report["project_path"]
    ).name

    coverage = (
        report["estimated_reuse_coverage"]
        * 100
    )

    similarity = (
        report["max_similarity"]
        * 100
    )

    st.markdown(
        f"## 📊 Project Reuse Analysis — {project_name}"
    )

    st.caption(
        "Estimated reuse coverage based on similarity "
        "of the analyzed source code to the new requirement."
    )

    a, b, c, d = st.columns(4)

    with a:

        st.metric(
            "Estimated Reuse Coverage",
            f"{coverage:.0f}%"
        )

    with b:

        st.metric(
            "Direct Reuse",
            f"{report['direct_loc']} LOC"
        )

    with c:

        st.metric(
            "Modify & Reuse",
            f"{report['modify_loc']} LOC"
        )

    with d:

        st.metric(
            "New Development",
            f"{report['new_loc']} LOC"
        )

    st.write("")

    st.write(
        f"**Requirement similarity:** "
        f"{similarity:.1f}%"
    )

    st.write(
        f"**Files analyzed:** "
        f"{report['analyzed_files']}"
    )

    st.write(
        f"**Analyzed code:** "
        f"{report['total_loc']} LOC"
    )

    st.divider()

    st.markdown(
        "### Components"
    )

    for component in report["components"][:10]:

        score = (
            component["score"]
            * 100
        )

        category = component["category"]

        if category == "Direct Reuse":

            icon = "✅"

        elif category == "Modify & Reuse":

            icon = "🔧"

        else:

            icon = "🆕"

        with st.container(
            border=True
        ):

            left, right = st.columns(
                [4, 1]
            )

            with left:

                st.write(
                    f"{icon} **{component['path']}**"
                )

                st.caption(
                    f"{category} • "
                    f"{component['loc']} LOC"
                )

            with right:

                st.write(
                    f"**{score:.1f}%**"
                )


def analyze_user_projects(query):

    projects = get_user_projects(
        st.session_state.user["id"]
    )

    reports = []

    for project in projects:

        project_path = project[3]

        try:

            report = analyze_project(
                project_path,
                query
            )

            report["project_name"] = project[1]

            reports.append(
                report
            )

        except Exception as error:

            print(
                f"Reuse analysis failed for "
                f"{project[1]}: {error}"
            )

    reports.sort(
        key=lambda item:
            item["estimated_reuse_coverage"],
        reverse=True
    )

    return reports




def process_query(query):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):

        with st.spinner(
            "RENOVA is analyzing your requirement..."
        ):

            try:

                public = search_public(query)

                private = search_private(query)

                reuse_reports = analyze_user_projects(
                    query
                )

                st.session_state.ai_queries += 1

                st.session_state.reuse_matches += (
                    len(public)
                    + len(private)
                )

                if (
                    not public
                    and not private
                    and not reuse_reports
                ):

                    response = (
                        "I couldn't find a relevant reusable "
                        "component or uploaded project for "
                        "this requirement."
                    )

                else:

                    response = (
                        f"I analyzed your requirement:\n\n"
                        f"> {query}\n\n"
                    )

                    if reuse_reports:

                        best_report = reuse_reports[0]

                        coverage = (
                            best_report[
                                "estimated_reuse_coverage"
                            ] * 100
                        )

                        response += (
                            f"📊 I analyzed "
                            f"{len(reuse_reports)} uploaded "
                            f"project(s). For "
                            f"{best_report['project_name']}, "
                            f"the estimated reuse coverage is "
                            f"{coverage:.0f}% based on the "
                            f"analyzed source code.\n\n"
                        )

                    if private:

                        response += (
                            f"🔒 Found {len(private)} "
                            f"matching component(s) in your "
                            f"uploaded projects.\n\n"
                        )

                    if public:

                        best = public[0]

                        response += (
                            f"🌐 Found {len(public)} "
                            f"relevant open-source "
                            f"component(s).\n\n"
                        )

                        response += (
                            f"Top semantic match: "
                            f"{best.get('func_name', 'Unnamed function')} "
                            f"with "
                            f"{best.get('score', 0):.1%} similarity."
                        )

                st.markdown(response)

                if reuse_reports:

                    st.markdown(
                        "### 📊 Project Reuse Analysis"
                    )

                    for report in reuse_reports:

                        show_reuse_report(report)

                if public:

                    st.markdown(
                        "### 🌐 Open-Source Matches"
                    )

                    for index, result in enumerate(
                        public,
                        1
                    ):

                        show_result(
                            result,
                            index,
                            "public"
                        )

                if private:

                    st.markdown(
                        "### 🔒 Your Project Matches"
                    )

                    for index, result in enumerate(
                        private,
                        1
                    ):

                        show_result(
                            result,
                            index,
                            "private"
                        )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "public": public,
                        "private": private,
                        "reuse_reports": reuse_reports,
                    }
                )

            except Exception as error:

                st.error(
                    f"RENOVA search error: {error}"
                )

# ============================================================
# SEARCH RESULT
# ============================================================

def show_result(
    result,
    number,
    source
):

    score = result.get(
        "score",
        0
    )

    if source == "public":

        title = result.get(
            "func_name",
            "Unnamed function"
        )

        st.markdown(
            f"### {number}. {title}"
        )

        st.write(
            f"**Similarity:** {score:.1%}"
        )

        st.write(
            f"**Repository:** "
            f"{result.get('repo', 'Unknown')}"
        )

        st.write(
            f"**File:** "
            f"{result.get('path', 'Unknown')}"
        )

        if result.get("docstring"):

            st.write(
                result["docstring"][:900]
            )

        with st.expander(
            "View source code"
        ):

            st.code(
                result.get(
                    "code",
                    ""
                ),
                language="python"
            )

        if result.get("url"):

            st.link_button(
                "Open on GitHub",
                result["url"]
            )

    else:

        st.markdown(
            f"### {number}. 🔒 "
            f"{result.get('project_name', 'Your Project')}"
        )

        st.write(
            f"**Similarity:** {score:.1%}"
        )

        st.write(
            f"**File:** "
            f"{result.get('path', 'Unknown')}"
        )

        with st.expander(
            "View matching code"
        ):

            st.code(
                result.get(
                    "content",
                    ""
                )[:15000],
                language="python"
            )


# ============================================================
# MY PROJECTS
# ============================================================

def my_projects():

    top_bar()

    st.markdown(
        "# 📁 My Projects"
    )

    st.caption(
        "Projects uploaded to your RENOVA account."
    )

    projects = get_user_projects(
        st.session_state.user["id"]
    )

    if not projects:

        st.info(
            "No projects uploaded yet."
        )

        return

    for project in projects:

        project_name = project[1]
        file_name = project[2]
        project_path = project[3]
        uploaded_at = project[4]

        st.markdown(
            f"### 📦 {project_name}"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.write(
                f"File: `{file_name}`"
            )

        with c2:

            st.write(
                f"Language: {get_language(project_path)}"
            )

        with c3:

            st.write(
                f"Files: {get_file_count(project_path)}"
            )

        st.caption(
            f"Uploaded: {uploaded_at}"
        )

        st.divider()


# ============================================================
# UPLOAD
# ============================================================


def upload_project():

    top_bar()

    st.markdown(
        "# ⬆️ Upload Project"
    )

    st.caption(
        "Upload previous projects to your private RENOVA knowledge base."
    )

    project_name = st.text_input(
        "Project Name",
        placeholder="Example: Face Recognition Attendance"
    )

    st.markdown(
        "### 📁 Choose your entire project folder"
    )

    st.caption(
        "Select the project folder directly. RENOVA will keep "
        "all uploaded files and subfolders."
    )

    uploaded_files = st.file_uploader(
        "Choose Project Folder",
        accept_multiple_files="directory",
        key="renova_project_folder",
        label_visibility="visible"
    )

    st.markdown(
        "### Or upload a ZIP file"
    )

    uploaded_zip = st.file_uploader(
        "Choose ZIP",
        type=["zip"],
        key="renova_project_zip",
        label_visibility="visible"
    )

    folder_selected = bool(uploaded_files)
    zip_selected = uploaded_zip is not None

    if folder_selected:

        st.success(
            f"📁 Selected project folder with "
            f"{len(uploaded_files)} file(s)."
        )

        with st.expander(
            "View selected files",
            expanded=False
        ):

            for file in uploaded_files:

                st.write(
                    f"• {file.name}"
                )

    elif zip_selected:

        st.success(
            f"📦 Selected ZIP: {uploaded_zip.name}"
        )

    if st.button(
        "⬆️ Upload Project",
        type="primary",
        use_container_width=True
    ):

        if not project_name.strip():

            st.error(
                "Enter a project name."
            )

            return

        if not folder_selected and not zip_selected:

            st.error(
                "Choose an entire project folder or a ZIP file."
            )

            return

        username = (
            st.session_state.user["username"]
        )

        folder = (
            UPLOAD_ROOT
            / safe_name(username)
            / safe_name(project_name)
        )

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        source = (
            folder
            / "source"
        )

        source.mkdir(
            parents=True,
            exist_ok=True
        )

        saved_file_count = 0

        try:

            if folder_selected:

                first_name = (
                    uploaded_files[0].name
                )

                normalized_first = (
                    first_name
                    .replace("\\", "/")
                    .strip("/")
                )

                first_parts = (
                    PurePosixPath(
                        normalized_first
                    ).parts
                )

                if len(first_parts) > 1:

                    original_folder_name = (
                        first_parts[0]
                    )

                else:

                    original_folder_name = (
                        project_name
                    )

                for uploaded_file in uploaded_files:

                    normalized_name = (
                        uploaded_file.name
                        .replace("\\", "/")
                        .strip("/")
                    )

                    parts = (
                        PurePosixPath(
                            normalized_name
                        ).parts
                    )

                    safe_parts = [
                        part
                        for part in parts
                        if part not in ("", ".", "..")
                    ]

                    if not safe_parts:
                        continue

                    # Streamlit directory uploads include
                    # the selected folder name as the first
                    # path component. Remove it so the
                    # contents are stored directly inside
                    # RENOVA's source folder.
                    if (
                        len(safe_parts) > 1
                        and safe_parts[0]
                        == original_folder_name
                    ):

                        relative_parts = (
                            safe_parts[1:]
                        )

                    else:

                        relative_parts = (
                            safe_parts
                        )

                    destination = (
                        source.joinpath(
                            *relative_parts
                        )
                    )

                    destination.parent.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    with open(
                        destination,
                        "wb"
                    ) as file:

                        file.write(
                            uploaded_file.getbuffer()
                        )

                    saved_file_count += 1

                if saved_file_count == 0:

                    st.error(
                        "No files were found in the selected folder."
                    )

                    return

                stored_name = (
                    f"{original_folder_name} "
                    f"({saved_file_count} files)"
                )

            else:

                destination = (
                    folder
                    / uploaded_zip.name
                )

                with open(
                    destination,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_zip.getbuffer()
                    )

                try:

                    with zipfile.ZipFile(
                        destination,
                        "r"
                    ) as archive:

                        archive.extractall(
                            source
                        )

                except zipfile.BadZipFile:

                    st.error(
                        "Invalid ZIP file."
                    )

                    return

                stored_name = (
                    uploaded_zip.name
                )

                saved_file_count = len(
                    [
                        item
                        for item in source.rglob("*")
                        if item.is_file()
                    ]
                )

            add_project(
                st.session_state.user["id"],
                project_name,
                stored_name,
                str(folder)
            )

            load_private_searcher.clear()

            st.success(
                f"✅ {project_name} uploaded successfully."
            )

            st.info(
                f"RENOVA stored {saved_file_count} "
                f"file(s) and preserved the project structure."
            )

            st.info(
                "Your project is now available to RENOVA AI Assistant."
            )

        except Exception as error:

            st.error(
                f"Upload failed: {error}"
            )

# ============================================================
# APPLICATION
# ============================================================

if st.session_state.user is None:

    login_page()

else:

    with st.sidebar:

        sidebar()

    if st.session_state.page == "Dashboard":

        dashboard()

    elif st.session_state.page == "AI Assistant":

        ai_assistant()

    elif st.session_state.page == "My Projects":

        my_projects()

    elif st.session_state.page == "Upload Project":

        upload_project()

    else:

        dashboard()
