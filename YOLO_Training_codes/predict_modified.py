import torch
import cv2
import hydra
from pathlib import Path
import easyocr
from torchvision.transforms import functional as F
from ultralytics.yolo.engine.predictor import BasePredictor, check_imgsz
from ultralytics.yolo.utils import DEFAULT_CFG_PATH, ops, plotting


reader = easyocr.Reader(['en'], gpu=True)

def perform_ocr_on_image(img, coordinates):
    x, y, w, h = map(int, coordinates)
    cropped_img = img[y:h, x:w]

    gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2GRAY)
    results = reader.readtext(gray_img)

    text = ""
    for res in results:
        if len(results) == 1 or (len(res[1]) > 6 and res[2] > 0.2):
            text = res[1]

    return str(text)


class DetectionPredictor(BasePredictor):

    def preprocess(self, img):
        img = F.to_tensor(img).to(self.model.device)
        img = img.half() if self.model.fp16 else img.float()
        img /= 255.0
        return img

    def postprocess(self, preds, img, orig_img):
        preds = ops.non_max_suppression(preds,
                                        self.args.conf,
                                        self.args.iou,
                                        agnostic=self.args.agnostic_nms,
                                        max_det=self.args.max_det)

        for i, pred in enumerate(preds):
            shape = orig_img[i].shape if self.webcam else orig_img.shape
            pred[:, :4] = ops.scale_boxes(img.shape[2:], pred[:, :4], shape).round()

        return preds

    def write_results(self, idx, preds, batch):
        p, im, im0 = batch
        log_string = ""

        if len(im.shape) == 3:
            im = im[None]

        self.seen += 1
        im0 = im0.copy()

        if self.webcam:
            log_string += f'{idx}: '
            frame = self.dataset.count
        else:
            frame = getattr(self.dataset, 'frame', 0)

        self.data_path = p
        self.txt_path = str(self.save_dir / 'labels' / p.stem) + ('' if self.dataset.mode == 'image' else f'_{frame}')
        log_string += '%gx%g ' % im.shape[2:]
        self.annotator = plotting.Annotator(im0, line_width=self.args.line_thickness, example=str(self.model.names))

        det = preds[idx]
        self.all_outputs.append(det)

        if len(det) == 0:
            return log_string

        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]

        for *xyxy, conf, cls in reversed(det):
            xyxy = [int(xy) for xy in xyxy]

            if self.args.save_txt:
                xywh = (ops.xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                line = (cls, *xywh, conf) if self.args.save_conf else (cls, *xywh)

                with open(f'{self.txt_path}.txt', 'a') as f:
                    f.write(('%g ' * len(line)).rstrip() % line + '/n')

            if self.args.save or self.args.save_crop or self.args.show:
                c = int(cls)
                label = None if self.args.hide_labels else (
                    self.model.names[c] if self.args.hide_conf else f'{self.model.names[c]} {conf:.2f}'
                )

                text_ocr = perform_ocr_on_image(im0, xyxy)
                label = text_ocr

                self.annotator.box_label(xyxy, label, color=plotting.colors(c, True))

            if self.args.save_crop:
                imc = im0.copy()
                plotting.save_one_box(
                    xyxy,
                    imc,
                    file=self.save_dir / 'crops' / self.model.model.names[c] / f'{self.data_path.stem}.jpg',
                    BGR=True
                )

        return log_string


@hydra.main(version_base=None, config_path=str(DEFAULT_CFG_PATH.parent), config_name=DEFAULT_CFG_PATH.name)
def predict(cfg):
    cfg.model = cfg.model or "C:/Users/aniru/Desktop/fresh/runs/detect/train/weights/best.pt"
    cfg.imgsz = check_imgsz(cfg.imgsz, min_dim=2)
    cfg.source = cfg.source if cfg.source is not None else "C:/Users/aniru/Desktop/fresh/a.mp4"
    predictor = DetectionPredictor(cfg)
    predictor()


if __name__ == "__main__":
    predict()
