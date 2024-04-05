from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import Disk
from app.diskUtils import get_unmounted_disks, mount, unmount, get_disk_usage, isMounted
import subprocess

router = APIRouter()
templates = Jinja2Templates(directory="templates")

MNT_PATH = "/mnt/share"

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if isMounted(MNT_PATH):
        usage = get_disk_usage(MNT_PATH)
        storage = {"free" : usage[0] - usage[1], "used" : usage[1]}
        return templates.TemplateResponse("homeMounted.html", { "request": request, "usage": storage})
    else:
        return templates.TemplateResponse("home.html", {"request": request})


def get_disk_list():
    disk_list = get_unmounted_disks()
    disks = []
    for disk in disk_list:
        disks.append(Disk(disk[0],disk[0], disk[1]))
    return disks

@router.get("/disks", response_class=HTMLResponse)
async def get_disks(request: Request):
    return templates.TemplateResponse("disks.html", {"request": request, "disks": get_disk_list()})

@router.post("/mount")
async def mount_disk(name : str, request: Request):
    mount(name, MNT_PATH)




@router.post("/unmount")
async def mount_disk(request: Request):
    unmount(MNT_PATH)
