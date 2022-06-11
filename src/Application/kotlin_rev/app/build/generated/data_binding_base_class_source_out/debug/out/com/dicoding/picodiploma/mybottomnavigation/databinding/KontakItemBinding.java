// Generated by view binder compiler. Do not edit!
package com.dicoding.picodiploma.mybottomnavigation.databinding;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.cardview.widget.CardView;
import androidx.viewbinding.ViewBinding;
import androidx.viewbinding.ViewBindings;
import com.dicoding.picodiploma.mybottomnavigation.R;
import de.hdodenhof.circleimageview.CircleImageView;
import java.lang.NullPointerException;
import java.lang.Override;
import java.lang.String;

public final class KontakItemBinding implements ViewBinding {
  @NonNull
  private final CardView rootView;

  @NonNull
  public final CardView cardView;

  @NonNull
  public final CircleImageView imgItemPhoto;

  @NonNull
  public final TextView tvItemName;

  @NonNull
  public final TextView tvItemUname;

  private KontakItemBinding(@NonNull CardView rootView, @NonNull CardView cardView,
      @NonNull CircleImageView imgItemPhoto, @NonNull TextView tvItemName,
      @NonNull TextView tvItemUname) {
    this.rootView = rootView;
    this.cardView = cardView;
    this.imgItemPhoto = imgItemPhoto;
    this.tvItemName = tvItemName;
    this.tvItemUname = tvItemUname;
  }

  @Override
  @NonNull
  public CardView getRoot() {
    return rootView;
  }

  @NonNull
  public static KontakItemBinding inflate(@NonNull LayoutInflater inflater) {
    return inflate(inflater, null, false);
  }

  @NonNull
  public static KontakItemBinding inflate(@NonNull LayoutInflater inflater,
      @Nullable ViewGroup parent, boolean attachToParent) {
    View root = inflater.inflate(R.layout.kontak_item, parent, false);
    if (attachToParent) {
      parent.addView(root);
    }
    return bind(root);
  }

  @NonNull
  public static KontakItemBinding bind(@NonNull View rootView) {
    // The body of this method is generated in a way you would not otherwise write.
    // This is done to optimize the compiled bytecode for size and performance.
    int id;
    missingId: {
      CardView cardView = (CardView) rootView;

      id = R.id.img_item_photo;
      CircleImageView imgItemPhoto = ViewBindings.findChildViewById(rootView, id);
      if (imgItemPhoto == null) {
        break missingId;
      }

      id = R.id.tv_item_name;
      TextView tvItemName = ViewBindings.findChildViewById(rootView, id);
      if (tvItemName == null) {
        break missingId;
      }

      id = R.id.tv_item_uname;
      TextView tvItemUname = ViewBindings.findChildViewById(rootView, id);
      if (tvItemUname == null) {
        break missingId;
      }

      return new KontakItemBinding((CardView) rootView, cardView, imgItemPhoto, tvItemName,
          tvItemUname);
    }
    String missingId = rootView.getResources().getResourceName(id);
    throw new NullPointerException("Missing required view with ID: ".concat(missingId));
  }
}
