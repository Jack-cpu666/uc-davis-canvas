from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>UC DAVIS Canvas</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link 
    rel="stylesheet" 
    href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
  >
  <style>
    /* RESET & BASE STYLES */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { font-family: 'Roboto', sans-serif; height: 100%; }
    body { display: flex; background-color: #F5F5F5; color: #333; }

    /* LEFT SIDEBAR (CANVAS GLOBAL NAVIGATION) */
    .sidebar {
      width: 70px;
      background-color: #2D3B45;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding-top: 20px;
    }
    .nav-item { position: relative; }
    .nav-link {
      width: 70px;
      height: 50px;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #fff;
      text-decoration: none;
      transition: background 0.3s;
      cursor: pointer;
    }
    .nav-link:hover { background: #394B59; }
    .nav-link svg { width: 24px; height: 24px; fill: #fff; }
    .sidebar .nav-item:not(:last-child) { margin-bottom: 10px; }

    /* SUBMENU (POP-OUT ON CLICK) */
    .submenu {
      display: none;
      position: absolute;
      left: 70px;
      top: 0;
      background-color: #394B59;
      padding: 10px 0;
      border-radius: 4px;
      min-width: 220px;
      z-index: 999;
    }
    .submenu ul { list-style: none; }
    .submenu ul li { border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
    .submenu ul li:last-child { border-bottom: none; }
    .submenu ul li a {
      display: block;
      padding: 8px 16px;
      color: #fff;
      text-decoration: none;
      transition: background-color 0.2s;
      cursor: pointer;
    }
    .submenu ul li a:hover { background-color: #4B5C6C; }
    .submenu.open { display: block; }

    /* MAIN CONTENT (TOP BAR + DASHBOARD) */
    .main {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    .topbar {
      height: 60px;
      background: #fff;
      border-bottom: 1px solid #e0e0e0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
    }
    .brand { display: flex; align-items: center; }
    .brand .ucd { font-size: 1.5rem; font-weight: 700; color: #002855; }
    .brand .canvas { font-size: 1.5rem; font-weight: 700; color: #FA3F2E; margin-left: 5px; }
    .user { font-size: 1rem; font-weight: 500; color: #555; }
    .dashboard {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
    }
    .dashboard h1 {
      font-size: 1.8rem;
      margin-bottom: 20px;
      color: #2D3B45;
    }

    /* COURSE CARDS GRID */
    .courses-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
    .course-card {
      background: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      display: flex;
      flex-direction: column;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
      cursor: pointer;
    }
    .course-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    .course-card-header {
      padding: 15px;
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
    }
    .course-card-header h2 {
      font-size: 1.1rem;
      font-weight: 700;
      color: #fff;
      margin: 0;
    }
    .course-card-body {
      padding: 15px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }
    .course-card-body .subtitle {
      font-size: 0.95rem;
      color: #777;
      margin-top: 8px;
    }
    .course-card-footer {
      margin-top: auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 15px;
      border-top: 1px solid #eee;
    }
    .grade {
      background: #002855;
      color: #fff;
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 0.9rem;
      font-weight: 600;
    }
    .dots {
      font-size: 1.4rem;
      color: #aaa;
      cursor: pointer;
      transition: color 0.2s;
    }
    .dots:hover { color: #888; }

    /* MODAL POPUP STYLES */
    .modal {
      display: none;
      position: fixed;
      z-index: 10000;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      overflow: auto;
      background-color: rgba(0,0,0,0.5);
      align-items: center;
      justify-content: center;
    }
    .modal-content {
      background-color: #fff;
      margin: auto;
      padding: 20px;
      border-radius: 8px;
      width: 80%;
      max-width: 700px;
      position: relative;
    }
    .close-btn {
      position: absolute;
      top: 10px;
      right: 15px;
      font-size: 1.2rem;
      background: none;
      border: none;
      cursor: pointer;
      color: #333;
    }
    .close-btn:hover { color: #666; }

    /* ASSIGNMENT LIST STYLES (inside modals) */
    .assignments {
      margin-top: 20px;
    }
    .assignment-item {
      padding: 10px 0;
      border-bottom: 1px solid #ddd;
    }
    .assignment-item:last-child {
      border-bottom: none;
    }
    .assignment-title {
      font-weight: 600;
      margin-bottom: 5px;
      color: #002855;
    }
    .assignment-details {
      font-size: 0.9rem;
      color: #555;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
    }
    .assignment-details span {
      margin-right: 10px;
    }
    .final-grade {
      margin-top: 15px;
      font-weight: 700;
      text-align: right;
      font-size: 1rem;
      color: #002855;
    }
  </style>
</head>
<body>
  <!-- SIDEBAR NAVIGATION with SUBMENUS -->
  <nav class="sidebar">
    <!-- ACCOUNT (has submenu) -->
    <div class="nav-item" data-menu="account">
      <a href="#" class="nav-link" title="Account">
        <svg viewBox="0 0 24 24">
          <path d="M12 2C6.477 2 2 6.477 2 12c0 5.523 
                   4.477 10 10 10s10-4.477 10-10C22 
                   6.477 17.523 2 12 2zm0 4c1.657 0 
                   3 1.343 3 3s-1.343 3-3 3-3-1.343-3-3 
                   1.343-3 3-3zm0 14c-2.33 0-4.396-1.043-5.803-2.68.03-1.72 
                   3.469-2.67 5.803-2.67 2.334 0 5.773.95 5.803 2.67C16.396 
                   18.957 14.33 20 12 20z"/>
        </svg>
      </a>
      <div class="submenu" id="submenu-account">
        <ul>
          <li><a href="#" onclick="openModal('profile');">Profile</a></li>
          <li><a href="#" onclick="openModal('settings');">Settings</a></li>
          <li><a href="#" onclick="openModal('notifications');">Notifications</a></li>
          <li><a href="#" onclick="openModal('files');">Files</a></li>
          <li><a href="#" onclick="openModal('eportfolios');">ePortfolios</a></li>
          <li><a href="#" onclick="openModal('logout');">Logout</a></li>
        </ul>
      </div>
    </div>

    <!-- DASHBOARD (no submenu) -->
    <div class="nav-item">
      <a href="#" class="nav-link" title="Dashboard" onclick="openModal('dashboard');">
        <svg viewBox="0 0 24 24">
          <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 
                   0h8V11h-8v10zm0-18v6h8V3h-8z"/>
        </svg>
      </a>
    </div>

    <!-- COURSES (has submenu) -->
    <div class="nav-item" data-menu="courses">
      <a href="#" class="nav-link" title="Courses">
        <svg viewBox="0 0 24 24">
          <path d="M3 4h18v2H3V4zm2 4h14v2H5V8zm-2
                   4h18v2H3v-2zm2 4h14v2H5v-2zm-2
                   4h18v2H3v-2z"/>
        </svg>
      </a>
      <div class="submenu" id="submenu-courses">
        <ul>
          <li><a href="#" onclick="openModal('cybr210');">CYBR 210: Cybersecurity Fundamentals</a></li>
          <li><a href="#" onclick="openModal('cybr310');">CYBR 310: Network Defense & Monitoring</a></li>
          <li><a href="#" onclick="openModal('cybr330');">CYBR 330: Ethical Hacking & Pen Testing</a></li>
          <li><a href="#" onclick="openModal('cybr340');">CYBR 340: Digital Forensics & Incident Response</a></li>
          <li><a href="#" onclick="openModal('cybr350');">CYBR 350: Malware Analysis & Reverse Engineering</a></li>
          <li><a href="#" onclick="openModal('cybr360');">CYBR 360: Security Policy & Risk Management</a></li>
          <hr style="margin: 5px 0;">
          <li><a href="#" onclick="openModal('allcourses');">All Courses</a></li>
        </ul>
      </div>
    </div>

    <!-- CALENDAR (no submenu) -->
    <div class="nav-item">
      <a href="#" class="nav-link" title="Calendar" onclick="openModal('calendar');">
        <svg viewBox="0 0 24 24">
          <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.1 
                   0-2 .9-2 2v14c0 1.1.9 2 2 
                   2h14c1.1 0 2-.9 2-2V5c0-1.1
                   -.9-2-2-2zm0 16H5V8h14v11z"/>
        </svg>
      </a>
    </div>

    <!-- INBOX (no submenu) -->
    <div class="nav-item">
      <a href="#" class="nav-link" title="Inbox" onclick="openModal('inbox');">
        <svg viewBox="0 0 24 24">
          <path d="M20 4H4c-1.1 0-2 .9-2 
                   2v12c0 1.1.9 2 2 2h16c1.1 
                   0 2-.9 2-2V6c0-1.1-.9-2
                   -2-2zm0 4l-8 5-8-5V6l8 
                   5 8-5v2z"/>
        </svg>
      </a>
    </div>

    <!-- HELP (has submenu) -->
    <div class="nav-item" data-menu="help">
      <a href="#" class="nav-link" title="Help">
        <svg viewBox="0 0 24 24">
          <path d="M12 2C6.476 2 2 6.476 
                   2 12c0 5.523 4.476 10 
                   10 10s10-4.477 10-10C22 
                   6.476 17.524 2 12 2zm1 
                   17h-2v-2h2v2zm1.07-7.75l
                   -.83.82c-.23.23-.37.5
                   -.37.83v.4h-2v-.4c0-.8.31
                   -1.56.88-2.12l1.13-1.13
                   c.18-.18.29-.44.29-.71 
                   0-.55-.45-1-1-1s-1 
                   .45-1 1h-2c0-1.66 1.34-3 
                   3-3s3 1.34 3 3c0 
                   .8-.31 1.56-.88 2.12z"/>
        </svg>
      </a>
      <div class="submenu" id="submenu-help">
        <ul>
          <li><a href="#" onclick="openModal('helpSearch');">Search Guides</a></li>
          <li><a href="#" onclick="openModal('helpProblem');">Report a Problem</a></li>
          <li><a href="#" onclick="openModal('helpQuestion');">Ask a Question</a></li>
          <li><a href="#" onclick="openModal('helpHotline');">Support Hotline</a></li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- MAIN CONTENT (TOP BAR + DASHBOARD) -->
  <div class="main">
    <!-- Top Bar -->
    <div class="topbar">
      <div class="brand">
        <div class="ucd">UC DAVIS</div>
        <div class="canvas">Canvas</div>
      </div>
      <div class="user">Ahmadullah Eshan</div>
    </div>

    <!-- Dashboard -->
    <div class="dashboard">
      <h1>Dashboard</h1>
      <div class="courses-grid">
        <!-- Course Card 1: CYBR 210 -->
        <div class="course-card" onclick="openModal('cybr210');" style="border-top: 4px solid #6A6EA9;">
          <div class="course-card-header" style="background-color:#6A6EA9;">
            <h2>CYBR 210: Cybersecurity Fundamentals</h2>
          </div>
          <div class="course-card-body">
            <div class="subtitle">Fall Quarter 2024</div>
            <div class="course-card-footer">
              <div class="grade">A - 93.45%</div>
              <div class="dots">&#8226;&#8226;&#8226;</div>
            </div>
          </div>
        </div>
        <!-- Course Card 2: CYBR 310 -->
        <div class="course-card" onclick="openModal('cybr310');" style="border-top: 4px solid #FA3F2E;">
          <div class="course-card-header" style="background-color:#FA3F2E;">
            <h2>CYBR 310: Network Defense & Monitoring</h2>
          </div>
          <div class="course-card-body">
            <div class="subtitle">Fall Quarter 2024</div>
            <div class="course-card-footer">
              <div class="grade">A - 94.23%</div>
              <div class="dots">&#8226;&#8226;&#8226;</div>
            </div>
          </div>
        </div>
        <!-- Course Card 3: CYBR 330 -->
        <div class="course-card" onclick="openModal('cybr330');" style="border-top: 4px solid #E27D60;">
          <div class="course-card-header" style="background-color:#E27D60;">
            <h2>CYBR 330: Ethical Hacking & Pen Testing</h2>
          </div>
          <div class="course-card-body">
            <div class="subtitle">Fall Quarter 2024</div>
            <div class="course-card-footer">
              <div class="grade">A - 95.88%</div>
              <div class="dots">&#8226;&#8226;&#8226;</div>
            </div>
          </div>
        </div>
        <!-- Course Card 4: CYBR 340 -->
        <div class="course-card" onclick="openModal('cybr340');" style="border-top: 4px solid #85DCB0;">
          <div class="course-card-header" style="background-color:#85DCB0;">
            <h2>CYBR 340: Digital Forensics & Incident Response</h2>
          </div>
          <div class="course-card-body">
            <div class="subtitle">Fall Quarter 2024</div>
            <div class="course-card-footer">
              <div class="grade">A - 96.67%</div>
              <div class="dots">&#8226;&#8226;&#8226;</div>
            </div>
          </div>
        </div>
        <!-- Course Card 5: CYBR 350 -->
        <div class="course-card" onclick="openModal('cybr350');" style="border-top: 4px solid #E8A87C;">
          <div class="course-card-header" style="background-color:#E8A87C;">
            <h2>CYBR 350: Malware Analysis & Reverse Engineering</h2>
          </div>
          <div class="course-card-body">
            <div class="subtitle">Fall Quarter 2024</div>
            <div class="course-card-footer">
              <div class="grade">A - 97.24%</div>
              <div class="dots">&#8226;&#8226;&#8226;</div>
            </div>
          </div>
        </div>
        <!-- Course Card 6: CYBR 360 -->
        <div class="course-card" onclick="openModal('cybr360');" style="border-top: 4px solid #C38D9E;">
          <div class="course-card-header" style="background-color:#C38D9E;">
            <h2>CYBR 360: Security Policy & Risk Management</h2>
          </div>
          <div class="course-card-body">
            <div class="subtitle">Fall Quarter 2024</div>
            <div class="course-card-footer">
              <div class="grade">A - 98.00%</div>
              <div class="dots">&#8226;&#8226;&#8226;</div>
            </div>
          </div>
        </div>
      </div><!-- .courses-grid -->
    </div><!-- .dashboard -->
  </div><!-- .main -->

  <!-- MODAL POPUP (DYNAMIC CONTENT) -->
  <div id="myModal" class="modal">
    <div class="modal-content">
      <button class="close-btn" onclick="closeModal()">&times;</button>
      <div id="modal-body">
        <!-- Content loaded dynamically via JavaScript -->
      </div>
    </div>
  </div>

  <!-- JAVASCRIPT FOR SUBMENU TOGGLE & MODAL CONTENT -->
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const navItems = document.querySelectorAll('.nav-item[data-menu]');
      navItems.forEach(item => {
        const link = item.querySelector('.nav-link');
        const submenu = item.querySelector('.submenu');
        link.addEventListener('click', (event) => {
          event.preventDefault();
          submenu.classList.toggle('open');
        });
      });
    });

    // Modal content with realistic UC Davis and cybersecurity details
    const modalContents = {
      // Account submenu
      'profile': `
        <h2>Profile</h2>
        <p><strong>Name:</strong> Ahmadullah Eshan</p>
        <p><strong>Email:</strong> aeshan@ucdavis.edu</p>
        <p><strong>Major:</strong> Cybersecurity</p>
        <p><strong>Year:</strong> Sophomore</p>
      `,
      'settings': `
        <h2>Settings</h2>
        <p>Update your UC Davis Canvas account settings:</p>
        <ul>
          <li>Change Password</li>
          <li>Notification Preferences</li>
          <li>Manage Linked Accounts</li>
        </ul>
      `,
      'notifications': `
        <h2>Notifications</h2>
        <ul>
          <li><strong>Prof. Nguyen</strong> – New assignment posted in <em>CYBR 340</em> due 2025-03-05.</li>
          <li><strong>UC Davis Admin</strong> – Scheduled maintenance this weekend.</li>
          <li><strong>Prof. Garcia</strong> – Reminder: Submit your project for <em>CYBR 310</em>.</li>
        </ul>
      `,
      'files': `
        <h2>Files</h2>
        <p>Access your course files and resources:</p>
        <ul>
          <li>Lecture Slides</li>
          <li>Assignment Guidelines</li>
          <li>Reference Documents</li>
        </ul>
      `,
      'eportfolios': `
        <h2>ePortfolios</h2>
        <p>Your ePortfolio showcases your projects and coursework. <a href="#">View your portfolio</a>.</p>
      `,
      'logout': `
        <h2>Logout</h2>
        <p>You have been successfully logged out from UC Davis Canvas. Thank you for visiting!</p>
      `,

      // Dashboard, Calendar, Inbox
      'dashboard': `
        <h2>Dashboard</h2>
        <p>Welcome to UC Davis Canvas – your central hub for course management, announcements, and deadlines.</p>
      `,
      'calendar': `
        <h2>Calendar</h2>
        <p>Upcoming UC Davis Events:</p>
        <ul>
          <li><strong>Career Fair</strong> – 2025-02-25</li>
          <li><strong>CYBR 340 Assignment Due</strong> – 2025-03-05</li>
          <li><strong>Campus Security Seminar</strong> – 2025-03-15</li>
        </ul>
      `,
      'inbox': `
        <h2>Inbox</h2>
        <p>Your recent messages:</p>
        <ul>
          <li><strong>Prof. Nguyen</strong> – New assignment in CYBR 340 posted <em>(2 hours ago)</em></li>
          <li><strong>UC Davis Admin</strong> – Canvas system update notice <em>(1 day ago)</em></li>
          <li><strong>Prof. Garcia</strong> – Reminder: Project deadline in CYBR 310 <em>(3 days ago)</em></li>
        </ul>
      `,

      // Courses – Assignment Details (Professional Assignment List Format)
      'cybr210': `
        <h2>CYBR 210 - Assignments</h2>
        <div class="assignments">
          <div class="assignment-item">
            <div class="assignment-title">Assignment 1: Introduction to Cybersecurity Concepts</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 88/100</span>
              <span class="assignment-weight">Weight: 10%</span>
              <span class="assignment-due">Due: 2025-02-10</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 2: History of Cyber Threats</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 90/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-18</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 3: Basic Security Policies</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 85/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-25</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 4: Analyzing Cyber Attacks</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 92/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-05</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 5: Security Tools Overview</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 90/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-03-12</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 6: Case Study Analysis</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 95/100</span>
              <span class="assignment-weight">Weight: 25%</span>
              <span class="assignment-due">Due: 2025-03-20</span>
            </div>
          </div>
        </div>
        <div class="final-grade">Overall Grade: 93.45% (A)</div>
      `,

      'cybr310': `
        <h2>CYBR 310 - Assignments</h2>
        <div class="assignments">
          <div class="assignment-item">
            <div class="assignment-title">Assignment 1: Network Architecture Analysis</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 90/100</span>
              <span class="assignment-weight">Weight: 12%</span>
              <span class="assignment-due">Due: 2025-02-12</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 2: Firewall Configuration Lab</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 92/100</span>
              <span class="assignment-weight">Weight: 18%</span>
              <span class="assignment-due">Due: 2025-02-20</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 3: Intrusion Detection Simulation</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 89/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-28</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 4: Packet Analysis Report</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 94/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-08</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 5: Network Monitoring Tools Review</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 91/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-15</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 6: Practical Network Defense Exercise</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 95/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-03-22</span>
            </div>
          </div>
        </div>
        <div class="final-grade">Overall Grade: 94.23% (A)</div>
      `,

      'cybr330': `
        <h2>CYBR 330 - Assignments</h2>
        <div class="assignments">
          <div class="assignment-item">
            <div class="assignment-title">Assignment 1: Reconnaissance Techniques</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 91/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-14</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 2: Vulnerability Scanning Lab</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 93/100</span>
              <span class="assignment-weight">Weight: 18%</span>
              <span class="assignment-due">Due: 2025-02-22</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 3: Exploit Development</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 90/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-03-01</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 4: Penetration Testing Report</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 95/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-10</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 5: Social Engineering Case Study</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 92/100</span>
              <span class="assignment-weight">Weight: 16%</span>
              <span class="assignment-due">Due: 2025-03-18</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 6: Secure System Hardening Exercise</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 96/100</span>
              <span class="assignment-weight">Weight: 16%</span>
              <span class="assignment-due">Due: 2025-03-25</span>
            </div>
          </div>
        </div>
        <div class="final-grade">Overall Grade: 95.88% (A)</div>
      `,

      'cybr340': `
        <h2>CYBR 340 - Assignments</h2>
        <div class="assignments">
          <div class="assignment-item">
            <div class="assignment-title">Assignment 1: Digital Evidence Collection</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 93/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-16</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 2: Forensic Analysis Lab</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 90/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-24</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 3: Incident Report Drafting</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 92/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-04</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 4: Malware Artifact Examination</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 94/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-03-12</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 5: Chain of Custody Documentation</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 91/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-03-18</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 6: Incident Response Simulation</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 95/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-26</span>
            </div>
          </div>
        </div>
        <div class="final-grade">Overall Grade: 96.67% (A)</div>
      `,

      'cybr350': `
        <h2>CYBR 350 - Assignments</h2>
        <div class="assignments">
          <div class="assignment-item">
            <div class="assignment-title">Assignment 1: Introduction to Reverse Engineering</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 90/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-14</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 2: Static Analysis Lab</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 92/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-22</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 3: Dynamic Analysis of Malware</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 89/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-02</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 4: Obfuscation Techniques Study</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 94/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-03-10</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 5: Malware Behavior Report</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 91/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-18</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 6: Reverse Engineering Challenge</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 95/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-03-26</span>
            </div>
          </div>
        </div>
        <div class="final-grade">Overall Grade: 97.24% (A)</div>
      `,

      'cybr360': `
        <h2>CYBR 360 - Assignments</h2>
        <div class="assignments">
          <div class="assignment-item">
            <div class="assignment-title">Assignment 1: Security Policy Drafting</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 92/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-16</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 2: Risk Assessment Exercise</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 90/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-02-24</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 3: Business Impact Analysis</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 91/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-04</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 4: Regulatory Compliance Review</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 93/100</span>
              <span class="assignment-weight">Weight: 20%</span>
              <span class="assignment-due">Due: 2025-03-12</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 5: Disaster Recovery Planning</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 90/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-03-20</span>
            </div>
          </div>
          <div class="assignment-item">
            <div class="assignment-title">Assignment 6: Security Audit Report</div>
            <div class="assignment-details">
              <span class="assignment-score">Score: 96/100</span>
              <span class="assignment-weight">Weight: 15%</span>
              <span class="assignment-due">Due: 2025-03-28</span>
            </div>
          </div>
        </div>
        <div class="final-grade">Overall Grade: 98.00% (A)</div>
      `,

      'allcourses': `
        <h2>All Courses</h2>
        <p>Manage your courses on UC Davis Canvas:</p>
        <ul>
          <li>CYBR 210: Cybersecurity Fundamentals</li>
          <li>CYBR 310: Network Defense & Monitoring</li>
          <li>CYBR 330: Ethical Hacking & Pen Testing</li>
          <li>CYBR 340: Digital Forensics & Incident Response</li>
          <li>CYBR 350: Malware Analysis & Reverse Engineering</li>
          <li>CYBR 360: Security Policy & Risk Management</li>
        </ul>
      `,

      // Help submenu
      'helpSearch': `
        <h2>Canvas Guides</h2>
        <p>Search the UC Davis Canvas Help Guides to learn how to navigate and use the system effectively.</p>
      `,
      'helpProblem': `
        <h2>Report a Problem</h2>
        <p>If you experience any issues with Canvas or your courses, please submit a support ticket. Our team is ready to assist you.</p>
      `,
      'helpQuestion': `
        <h2>Ask a Question</h2>
        <p>Need help? Use Canvas messaging to reach out to your instructor with any questions.</p>
      `,
      'helpHotline': `
        <h2>Canvas Support Hotline</h2>
        <p>For immediate assistance, call the UC Davis Canvas Support Hotline at (530) 752-XXXX.</p>
      `
    };

    function openModal(key) {
      const modal = document.getElementById('myModal');
      const modalBody = document.getElementById('modal-body');
      modalBody.innerHTML = modalContents[key] || '<h2>Content Not Found</h2><p>No content available for this section.</p>';
      modal.style.display = 'flex';
    }

    function closeModal() {
      document.getElementById('myModal').style.display = 'none';
    }

    window.onclick = function(event) {
      const modal = document.getElementById('myModal');
      if (event.target === modal) {
        modal.style.display = 'none';
      }
    }
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    # Run the app on 0.0.0.0 to be accessible from your cloud host
    app.run(host='0.0.0.0', port=8080, debug=True)
